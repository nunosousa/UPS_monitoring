import polars
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

#dataset format:
# %TIME @Y@m@d @H@M@S% %VAR battery.charge% %VAR input.voltage% %VAR ups.load% [%VAR ups.status%] %VAR ups.temperature% %VAR input.frequency%
# 20250109 180822 NA 222.0 2 [OL BYPASS] 29.0 50.0

# ups.status values:
# OL      -- On line (mains is present)
# OB      -- On battery (mains is not present)
# LB      -- Low battery
# HB      -- High battery
# RB      -- The battery needs to be replaced
# CHRG    -- The battery is charging
# DISCHRG -- The battery is discharging (inverter is providing load power)
# BYPASS  -- UPS bypass circuit is active -- no battery protection is available
# CAL     -- UPS is currently performing runtime calibration (on battery)
# OFF     -- UPS is offline and is not supplying power to the load
# OVER    -- UPS is overloaded
# TRIM    -- UPS is trimming incoming voltage (called "buck" in some hardware)
# BOOST   -- UPS is boosting incoming voltage
# FSD     -- Forced Shutdown (restricted use, see the note below)

ups_data_frame = polars.read_csv(
    "dataset/upslog.txt",
    infer_schema=True,
    has_header=False,
    separator=" ",
    decimal_comma=False,
    columns=[0, 3, 4, 5, 6, 7, 8, 9, 10],
    quote_char="%")

ups_data_frame = ups_data_frame.rename({"column_1": "DateTime",
                                        #"column_2": "Date",
                                        #"column_3": "Time",
                                        "column_4": "battery.voltage",
                                        "column_5": "input.frequency",
                                        "column_6": "input.voltage",
                                        "column_7": "input.voltage.fault",
                                        "column_8": "output.voltage",
                                        "column_9": "ups.load",
                                        "column_10": "ups.status",
                                        "column_11": "ups.temperature"})

#Convert the first column to a date format
ups_data_frame = ups_data_frame.with_columns(
    polars.from_epoch(polars.col("DateTime"), time_unit="s"))

ups_data_frame = ups_data_frame.with_columns(
    polars.col("DateTime").dt.date().alias("Date"))
    #polars.col("Date").cast(polars.String).str.to_date("%Y%m%d"))

ups_data_frame = ups_data_frame.with_columns(
    polars.col("DateTime").dt.time().alias("Time"))
    #polars.col("Time").cast(polars.String).str.to_time("%H%M%S"))

print(ups_data_frame)

#Determine the unique dates in the dataset
dates = ups_data_frame.unique(subset="Date", maintain_order=True)
num_dates = dates.height

# Norma CEI 38 2003+
# 230 V -10% +6% (entre 207V e 243,8V)
cei38_high = 243.8
cei38_low = 207.0

for i in range(num_dates):
    ups_data_frame_day = ups_data_frame.filter(polars.col("Date") == dates.item(i, "Date"))

    x_cei38 = [ups_data_frame_day["DateTime"].item(0), ups_data_frame_day["DateTime"].item(ups_data_frame_day.height-1)]
    y_high_cei38 = [cei38_high, cei38_high]
    y_low_cei38 = [cei38_low, cei38_low]

    fig = plt.figure("EuroTech SMART UPS 640VA [" + str(dates.item(i, "Date")) + "]")


    ax1 = fig.add_subplot(2, 1, 1)

    ax1.plot(ups_data_frame_day["DateTime"], ups_data_frame_day["input.voltage"], label='Input')
    ax1.plot(ups_data_frame_day["DateTime"], ups_data_frame_day["output.voltage"], label='Output')
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
    ax1.set_ylim(top=cei38_high+4, bottom=cei38_low-4)
    ax1.set_xlim(left=x_cei38[0], right=x_cei38[1])
    ax1.set_xlabel('Time')
    ax1.set_ylabel('Voltage [V]')
    ax1.set_title('Mains voltage on ' + str(dates.item(i, "Date")))

    ax1.plot(x_cei38, y_high_cei38, '-.', label='CEI 38-2003+ 243.8V')
    ax1.plot(x_cei38, y_low_cei38, '-.', label='CEI 38-2003+ 207V')
    ax1.legend(loc="best")


    ax2 = fig.add_subplot(2, 1, 2)

    ax2.set_xlabel('Time')

plt.show()

