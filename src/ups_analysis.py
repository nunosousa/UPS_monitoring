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


print(ups_data_frame.unique(subset="Date", maintain_order=True))
print(ups_data_frame.filter(polars.col("Date") == polars.lit("2025-01-04").str.to_date()))

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.plot(ups_data_frame["Voltage"])
plt.show()

