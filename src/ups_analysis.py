import polars
import matplotlib.pyplot as plt

#dataset format:
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

ups_data_frame = ups_data_frame.rename({"column_1": "Date", "column_2": "Time","column_4": "Voltage"})

dates = ups_data_frame.unique(subset="Date", maintain_order=True)
num_dates = dates.height

for i in range(num_dates):
    ups_data_frame_day = ups_data_frame.filter(polars.col("Date") == dates.item(i, 0))

    fig = plt.figure(i)
    ax1 = fig.add_subplot(1, 1, 1)
    ax1.plot(ups_data_frame_day["Voltage"])
    ax1.set_xlabel('Time')
    ax1.set_ylabel('Voltage [V]')
    ax1.set_title('Mains voltage on ' + str(dates.item(i, 0)))

plt.show()

