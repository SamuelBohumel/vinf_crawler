from pyspark.sql import SparkSession
import os

def process_text_file(file_path):
    # Your processing logic for each text file goes here
    # Example: Read the text file and count the number of lines
    with open(file_path, 'r', encoding='utf8') as file:
        lines_count = len(file.readlines())

    return file_path, lines_count

def main():
    # Initialize Spark session
    spark = SparkSession.builder.appName("TextFilesProcessing").getOrCreate()
    print("Starting")
    try:
        # List of text files to process
        files = []
        for text_file in os.listdir(os.path.join("results", "articles")):
            files.append(os.path.join("results", "articles", text_file))

        # Create an RDD from the list of text files
        text_files_rdd = spark.sparkContext.parallelize(files)

        # Process each text file using the function defined above
        results = text_files_rdd.map(process_text_file).collect()

        # Display the results
        for file_path, lines_count in results:
            print(f"File: {file_path}, Lines Count: {lines_count}")

    finally:
        # Stop the Spark session
        spark.stop()

if __name__ == "__main__":
    main()
