import polars
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

#dataset format:
# %TIME @Y@m@d @H@M@S% %VAR battery.charge% %VAR input.voltage% %VAR ups.load% [%VAR ups.status%] %VAR ups.temperature% %VAR input.frequency%
# 20250109 180822 NA 222.0 2 [OL BYPASS] 29.0 50.0

ups_data_frame = polars.read_csv(
    "dataset/upslog.txt",
    infer_schema=False,
    has_header=False,
    separator=" ",
    decimal_comma=False,
    columns=[0, 1, 3],
    quote_char="\"")

#Convert the first column to a date format
ups_data_frame = ups_data_frame.with_columns(
    polars.col("column_1").cast(polars.String).str.to_date("%Y%m%d"))

ups_data_frame = ups_data_frame.with_columns(
    polars.col("column_2").cast(polars.String).str.to_time("%H%M%S"))

ups_data_frame = ups_data_frame.with_columns(
    polars.col("column_4").cast(polars.Float32))

ups_data_frame = ups_data_frame.with_columns(
    polars.col("column_1").dt.combine(polars.col("column_2")).alias("DateTime"))

ups_data_frame = ups_data_frame.rename({"column_1": "Date", "column_2": "Time","column_4": "Voltage"})

dates = ups_data_frame.unique(subset="Date", maintain_order=True)
num_dates = dates.height


for i in range(num_dates):
    ups_data_frame_day = ups_data_frame.filter(polars.col("Date") == dates.item(i, 0))
    #print(ups_data_frame_day)

    # Norma CEI 38 2003+
    # 230 V -10% +6% (entre 207V e 243,8V)
    cei38_high = 243.8
    cei38_low = 207.0

    x_cei38 = [ups_data_frame_day["DateTime"].item(0), ups_data_frame_day["DateTime"].item(ups_data_frame_day.height-1)]
    y_high_cei38 = [cei38_high, cei38_high]
    y_low_cei38 = [cei38_low, cei38_low]

    fig = plt.figure("EuroTech SMART UPS 640VA [" + str(dates.item(i, 0)) + "]")


    ax1 = fig.add_subplot(2, 1, 1)

    #ax1.plot(ups_data_frame_day["Voltage"], label='Voltage')
    ax1.plot(ups_data_frame_day["DateTime"], ups_data_frame_day["Voltage"], label='Voltage')
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
    ax1.set_ylim(top=cei38_high+4, bottom=cei38_low-4)
    ax1.set_xlim(left=x_cei38[0], right=x_cei38[1])
    ax1.set_xlabel('Time')
    ax1.set_ylabel('Voltage [V]')
    ax1.set_title('Mains voltage on ' + str(dates.item(i, 0)))

    ax1.plot(x_cei38, y_high_cei38, '-.', label='CEI 38-2003+ 243.8V')
    ax1.plot(x_cei38, y_low_cei38, '-.', label='CEI 38-2003+ 207V')
    ax1.legend(loc="best")


    ax2 = fig.add_subplot(2, 1, 2)

    ax2.set_xlabel('Time')

plt.show()

