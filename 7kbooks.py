#Program to analyse data set
#The dataset is called 7kBooks and the original version can be found at the following location:
#https://www.kaggle.com/dylanjcastillo/7k-books-with-metadata
print("This program performs analysis on a dataset of books")
print("The dataset is called 7kBooks and the original version can be found at the following location:")
print("https://www.kaggle.com/dylanjcastillo/7k-books-with-metadata")
print()

import matplotlib.pyplot as plt
from math import sqrt

def get_data(filename):
    """
    A function to open the 7KBooks.csv file and generate lists/dictionaries for analysis

    Parameters
    ----------
    filename : string
        A file location containing book information.

    Returns
    -------
    processed_page_numbers : list
        A list of page numbers per book processed to remove empty values and converted to float.
    year_list : list
        A list of published years per book processed to remove empty values and converted to float.
    processed_average_rating : list
        A list of average ratings per book processed to remove empty values and converted to float.
    processed_number_of_ratings : list
        A list of the number of ratings per book processed to remove empty values and converted to float.
    title_and_page_num : dict
        A dictionary containing a book title and the number of pages in the book as a key-value pair.

    """
    #create empty lists and dictionaries to populate
    page_numbers_list = []
    year_list = []
    average_rating_list = []
    number_of_ratings_list = []
    title_and_page_num = {}
    
    #open the file
    with open(filename, encoding="utf8") as books:
        #ignore the first line with the column titles
        books.readline()
        #read in each other line and split into columns
        for line in books:
            isbn13, isbn10, title, subtitle, authors, categories, thumbnail, description, year, average_rating, pages, ratings= line.split(",")
            page_numbers_list.append(pages)
            average_rating_list.append(average_rating)
            
            #strip \n from end of last column
            number_of_ratings_list.append(ratings.strip())
            year_list.append(year)
            
            #convert any items in pages that are empty to zero
            convert_blank_to_zero(page_numbers_list)
            convert_blank_to_zero(average_rating_list)
            convert_blank_to_zero(number_of_ratings_list)
            
            #convert field in list to be unknown if the year is missing
            for i in range(len(page_numbers_list)):
                    if year_list[i] == '':
                        year_list[i] = "Unknown"
            
            #convert the items in the list to floats so calculations can be done on them
            processed_page_numbers = convert_list_of_strings_to_floats(page_numbers_list)
            processed_average_rating = convert_list_of_strings_to_floats(average_rating_list)
            processed_number_of_ratings = convert_list_of_strings_to_floats(number_of_ratings_list)
            
            #change + to commas in title and processed_pages dictionary
            if title not in title_and_page_num:
                if "+" not in title: 
                    title_and_page_num[title] = pages
                else:
                    edited_title = title.replace("+", ",")
                    title_and_page_num[edited_title] = pages
    
    return processed_page_numbers, year_list, processed_average_rating, processed_number_of_ratings, title_and_page_num
    
def get_top_ten_longest_books(dict_of_title_and_pages):
    """
    A function to get the top ten books with the most pages
 
    Parameters
    ----------
    dict_of_title_and_pages : dict
        A dictionary of title and page numbers in key value pairs.

    Returns
    -------
    top_ten: list
        A list of the top ten book titles and their page lengths

    """
    #create a copy of the dictionary and sort it by page number
    dict_copy = dict_of_title_and_pages.copy()
    #sort the copy
    sorted_dict = {k: v for k, v in sorted(dict_copy.items(), key=lambda x: x[1], reverse=True)}
    
    #get the top ten items in the sorted list
    top_ten = dict(list(sorted_dict.items())[0:10])
    
    return top_ten

def get_books_with_same_number_pages_as_mean(list_of_page_numbers, dict_of_title_and_pages):
    """
    A function to display the book titles that have the same number of pages as the mean

    Parameters
    ----------
    list_of_page_numbers : listDict
        A list of book page numbers
    dict_of_title_and_pages : dict
        A dictionaty of titles and page numbers in key value pairs.

    Returns
    -------
    None.

    """
    #create a copy of the dictionary
    dict_copy = dict_of_title_and_pages.copy()
    
    #get the mean value of page numbers converted to int for whole number of pages
    mean_value = int(round(calculate_mean(list_of_page_numbers),0))
    
    print(f"    {' Pages':>5}{'Title':>10}")
    for title, pages in dict_copy.items():
        if pages == mean_value:
            print("   - ", pages, "   ", title)
        else:
            continue

    
def get_total_number_of_records_in_list(list_of_records):
    """
    A function to get the total number of records in a list
    
    Parameters
    ----------
    list_of_records : list
        A list of records

    Returns
    -------
    number_of_records : int
        The number of records in the list.

    """
    number_of_records = len(list_of_records)
    
    return round(number_of_records, 0)

def get_max_value(list_of_records):
    """
    A function to get the maximum value in a list of records
    
    Parameters
    ----------
    list_of_records : list
        a list of records

    Returns
    -------
    max_value: int
        The maximum value for a record in the list.

    """
    max_value = max(list_of_records)
    
    return int(max_value)
    
def get_fewest_pages_excluding_zero(list_of_records):
    """
    A function to get the smallest number of pages in a book excluding zero
    
    Parameters
    ----------
    list_of_records : list
        A list of pages per book

    Returns
    -------
    fewest_pages : int
        The fewest pages for a record not including zero.

    """
    fewest_pages = 9999
    #loop through the list
    for i in list_of_records:  
        #ignore values in the list with zero
        if i == 0:
            continue
        elif i < fewest_pages:
            #if the value is less than fewest_pages the value is the new lowest value
            fewest_pages = i
            
    return int(fewest_pages)

def get_most_recent_year(list_of_years):
    """
    A function that takes a list of years and returns the most recent year

    Parameters
    ----------
    list_of_years : list
        A list of years.

    Returns
    -------
    most_recent_year: int
        The most recent year a book was published in the list
    """
    #set intial highest year to be 1
    most_recent_year = 1
    for item in list_of_years:
        #ignore items with no year
        if item == "Unknown":
            continue
        else:
         #convert year to int to compare values
            int_item = int(item)
            if int_item > most_recent_year:
                most_recent_year = int_item
                
    return most_recent_year
            
def get_book_with_fewest_pages(list_of_books_and_pages):
    """
    A function that takes determines the book with the fewest pages in the list excluding those with zero

    Parameters
    ----------
    list_of_books_and_pages : dict
        A dictionary with book title and number of pages in a key value pair.

    Returns
    -------
    title_with_fewest_pages: int
         The title of the book with the most pages

    """
    #set the fewest pages
    fewest_pages = 9999
    #convert the valeus in the dictionary to int
    converted_dict = convert_dictionary_values_to_int_from_string(list_of_books_and_pages)
    
    #loop through the converted dictionary for the lowest value that is not zero
    for item in converted_dict:
        if converted_dict[item] < fewest_pages and converted_dict[item] > 0:
            fewest_pages = converted_dict[item]
    
    #get the associated key for the lowest value
    for key, value in converted_dict.items():
        if value == fewest_pages:
            title_with_fewest_pages = key
    
    return title_with_fewest_pages.title()
    
def get_book_with_most_pages(list_of_books_and_pages):
    """
    A function that takes determines the book with the most pages in the list

    Parameters
    ----------
    list_of_books_and_pages : dict
        A dictionary with book title and number of pages in a key value pair.

    Returns
    -------
    title_with_most_pages: string
        The title of the book with the most pages

    """
    #convert string values in the dictionary to ints to allow for calculations
    converted_dict = convert_dictionary_values_to_int_from_string(list_of_books_and_pages)
    
    title_with_most_pages = max(converted_dict, key=converted_dict.get) 
    
    return title_with_most_pages

def convert_dictionary_values_to_int_from_string(dictionary_of_records):
    """
    A function to convert string values to ints in a dictionary of key value pairs

    Parameters
    ----------
    dictionary_of_records : dict
        A dictionary of key value pairs in string format.

    Returns
    -------
    dictionary_of_records : dict
        A dictionary of key value pairs in string - int format.

    """
    #convert string values for pages to int in dictionary
    for item in dictionary_of_records:
        #if the string in empty change it to zero
        if dictionary_of_records[item] == '':
            dictionary_of_records[item] = 0
        else:
            #if the string is not empty convert it to an int
            dictionary_of_records[item] = int(dictionary_of_records[item])
            
    return dictionary_of_records

def get_number_of_items_with_missing_information(list_of_records): 
    """
    A function to get the number of items in a column with missing information
    
    Parameters
    ----------
    list_of_records : list
        A list of items from one column in the csv file.

    Returns
    -------
    counter : int
        The number of records in the list with no value.

    """
    counter = 0
    #count the number of items that have 0 value
    for record in list_of_records:
        if record == 0:
            counter += 1
            
    return counter

def convert_blank_to_zero(list_with_empty_values):
    """
    A function for pre-processing data to change and empty values to zero
    
    Parameters
    ----------
    list_with_empty_values : list
        A list with some empty values

    Returns
    -------
    None.

    """
    #convert items with no value to 0
    for i in range(len(list_with_empty_values)):
        if list_with_empty_values[i] == '':
            list_with_empty_values[i] = "0"

def convert_list_of_strings_to_floats(list_of_strings):
    """
    A function for pre-processing data to convert the items in the list from string to float
    
    Parameters
    ----------
    list_of_strings : list
        A list of numbers in string format

    Returns
    -------
    list_of_floats: list
        A list of the numbers in the original list converted to floats

    """
    list_of_floats = [float(x) for x in list_of_strings]
    
    return list_of_floats
    
def count_of_unique_items_in_list(list_of_items):
    """
    A function for counting the number times each item appears in the list
    
    Parameters
    ----------
    list_of_items : list
        A list of items.

    Returns
    -------
    count_list : list
        A list of the count of each number of items in the original list.

    """
    count_list = []
    
    for item in list_of_items:
        count = list_of_items.count(item)
        #add count of items to new list with number of times it occurs in the list
        if [item, count] not in count_list:
            count_list.append([item, count])
        else:
            continue
        
    return count_list
    
def display_published_years(years):
    """
    A function to display visualizations for published years
    
    Parameters
    ----------
    years : list
        a list of published years.

    Returns
    -------
    None.
    

    """
    #get the count of each unique year in the list
    count_of_years = count_of_unique_items_in_list(years)
    
    #sort the list of years and counts
    sorted_list = sorted(count_of_years, key=lambda x: x[1], reverse=True)
    #convert to a dictionary with only the first 10 items from the sorted
    year_dict = dict(sorted_list[:10])
    
    #sort the dictionary as well to make sure it is correct
    sorted_year_dict = {}
    sorted_keys = sorted(year_dict, key=year_dict.get, reverse=True)
    
    #put the sorted items into a dictionary for use in the plot
    for item in sorted_keys:
        sorted_year_dict[item] = year_dict[item]
    
    #as a pie chart
    fig, ax = plt.subplots()
    ax.set_title("Top Ten Years for Published Books")
    ax.pie(sorted_year_dict.values(), labels=sorted_year_dict.keys(), autopct="%.0f%%")
    plt.show()
    
    #save the chart as a png file
    fig.savefig("top_ten_published_years.png", bbox_inches="tight")

def display_visual_page_number_statistics(list_of_page_info):
    """
    A function to visually display the results of the statistical analysis of the page number variable in a bar chart

    Parameters
    ----------
    list_of_page_info : list
        A list of page numbers.

    Returns
    -------
    None.

    """
    #get the statistical results for page numbers
    pages_mean = calculate_mean(list_of_page_info)
    pages_sd = calculate_standard_deviation(list_of_page_info)
    pages_mode = calculate_mode(list_of_page_info)
    pages_median = calculate_median(list_of_page_info)
    
    #create a dictionary of statistical results
    pages_data = {'Mean':pages_mean,
                  'Standard Deviation':pages_sd,
                  'Mode':pages_mode,
                  'Median':pages_median}
    
    fig, ax = plt.subplots()
    
    #plot page number analysis
    ax.set_title("Page Number Analysis")
    
    y_pos = [i for i in range(len(pages_data))]
    
    ax.set_yticks(y_pos)
    ax.set_yticklabels(pages_data.keys())
    
    ax.set_ylabel("Type of Analysis")
    ax.set_xlabel("Number of pages")

    ax.barh(y_pos, pages_data.values(), align="center")
    
    plt.show() 
    
    fig.savefig("page_number_statistics.png", bbox_inches="tight")

def display_visual_number_of_ratings_statistics(list_of_number_ratings):
    """
    A function to visually display the statistical analysis results for the number of ratings variable in a bar chart

    Parameters
    ----------
    list_of_number_ratings : list
        A list of the number of ratings for each book.

    Returns
    -------
    None.

    """
    #get the statistical results for number of ratings
    number_ratings_mean = calculate_mean(list_of_number_ratings)
    number_ratings_sd = calculate_standard_deviation(list_of_number_ratings)
    number_ratings_mode = calculate_mode(list_of_number_ratings)
    number_ratings_median = calculate_median(list_of_number_ratings)
    
    #create a dictionary of statistical results
    number_ratings_data = {'Mean':number_ratings_mean,
                  'Standard Deviation':number_ratings_sd,
                  'Mode':number_ratings_mode,
                  'Median':number_ratings_median}
    
    fig, ax = plt.subplots()
    
    #plot number of ratings analysis
    ax.set_title("Number of Ratings Analysis")
    
    y_pos = [i for i in range(len(number_ratings_data))]
    
    ax.set_yticks(y_pos)
    ax.set_yticklabels(number_ratings_data.keys())
    
    ax.set_ylabel("Analysis")
    ax.set_xlabel("Result")
    
    ax.barh(y_pos, number_ratings_data.values(), align="center")
    
    plt.show() 
    
    fig.savefig("number_of_reviews_statistics.png", bbox_inches="tight")
    
def display_visual_average_rating_statistics(list_of_ratings_info):
    """
    A function to visually display the statistical analysis results for the average ratings variable in a bar chart

    Parameters
    ----------
    list_of_ratings_info : list
        A list of average ratings.

    Returns
    -------
    None.

    """
    #get the statistical results for average ratings
    av_ratings_mean = calculate_mean(list_of_ratings_info)
    av_ratings_sd = calculate_standard_deviation(list_of_ratings_info)
    av_ratings_mode = calculate_mode(list_of_ratings_info)
    av_ratings_median = calculate_median(list_of_ratings_info)
    
    #create a dictionary of statistical results
    av_ratings_data = {'Mean':av_ratings_mean,
                  'Standard Deviation':av_ratings_sd,
                  'Mode':av_ratings_mode,
                  'Median':av_ratings_median}
    
    fig, ax = plt.subplots()
    
    #plot average rating analysis
    ax.set_title("Average Rating Analysis")
    
    y_pos = [i for i in range(len(av_ratings_data))]
    
    ax.set_yticks(y_pos)
    ax.set_yticklabels(av_ratings_data.keys())
    
    ax.set_ylabel("Type of Analysis")
    ax.set_xlabel("Average Rating")
    
    ax.barh(y_pos, av_ratings_data.values(), align="center")
    
    plt.show()  
    
    #save the file as a png
    fig.savefig("average_rating_statistics.png", bbox_inches="tight")
    
def display_scatter_plot(list_of_page_numbers, list_of_average_ratings):
    """
    A function to visually display the average rating v number of pages in a scatter chart

    Parameters
    ----------
    list_of_page_numbers : list
        A list of page numbers per book.
    list_of_average_ratings : list
        A list of average ratings per book.

    Returns
    -------
    None.

    """
    fig, ax = plt.subplots()
    
    ax.set_xlabel("Number of Pages in Book")
    ax.set_ylabel("Average Rating of Book")
    
    ax.set_title("Average Rating & Number of Pages")
    
    #create the scatter using the page number and average rating lists
    ax.scatter(list_of_page_numbers, list_of_average_ratings, marker=".")
    
    plt.show()
    
    #save the file as a png
    fig.savefig("page_number_v_average_rating.png", bbox_inches="tight")
    
def display_top_ten_longest_books(dict_of_title_and_pages):
    """
    A function to visually display the top ten longest tiles and their number of pages

    Parameters
    ----------
    dict_of_title_and_pages : dict
        A dictionary of titles and page numbers in key value pair.

    Returns
    -------
    None.

    """
    #convert strings to ints in the dictionary
    dict_with_ints = convert_dictionary_values_to_int_from_string(dict_of_title_and_pages)
    #get the top ten longest books in the dictionary
    top_ten = get_top_ten_longest_books(dict_with_ints)
    
    fig, ax = plt.subplots()
    
    #plot average rating analysis
    ax.set_title("Top Ten Longest Books")
    
    y_pos = [i for i in range(len(top_ten))]
    
    ax.set_yticks(y_pos)
    #set limit on size of text due to long book titles
    ax.set_yticklabels(top_ten.keys(), size=7)
    
    ax.set_ylabel("Book Title")
    ax.set_xlabel("Number of Pages")
    
    #create the bar chart
    ax.barh(y_pos, top_ten.values(), align="center")
    
    plt.show()  
    
    #save the file as a png
    fig.savefig("top_ten_longest_books.png", bbox_inches="tight")
    
def calculate_mean(list_of_records):
    """
    A function to calculate the mean from a list of values

    Parameters
    ----------
    list_of_records : list
        A list of records in float format.

    Returns
    -------
    mean_value: float
        The mean value of the original list

    """
    mean_value = sum(list_of_records)/len(list_of_records)
    return mean_value
    
def calculate_standard_deviation(list_of_records):
    """
    A function to calculate the standard deviation of a list of records

    Parameters
    ----------
    list_of_records : list
        A list of record in float format.

    Returns
    -------
    standard_deviation_value:
        The standard deviation for the original list

    """
    deviations = [(x - calculate_mean(list_of_records)) ** 2 for x in list_of_records] 
    standard_deviation = sqrt(sum(deviations)/(len(list_of_records)))
    
    return standard_deviation

def calculate_median(list_of_records):
    """
    A function to calculate the median of a list of records

    Parameters
    ----------
    list_of_records : list
        A list of records in float format.

    Returns
    -------
    median_value: float.
        The value of the median in the original list
    """
    #create a copy of the list for the sorting to be used in the calculation in order to preserve the order of the original list
    copy_of_list = list_of_records.copy()
    mid_index = int(len(copy_of_list)/2)
    copy_of_list.sort()
    
    if len(copy_of_list) % 2:
        median_value = copy_of_list[mid_index]
    else:
        median_value = (copy_of_list[mid_index-1] + copy_of_list[mid_index]) / 2
    
    return median_value

def calculate_mode(list_of_records):
    """
    A function to calculate the mode of a list

    Parameters
    ----------
    list_of_records : list
        A list of records in float format

    Returns
    -------
    mode_value: float
        The value of the mode of the original list

    """
    #create a copy of the list for use in the calculations so the original list maintains its order
    copy_of_list = list_of_records.copy()
    count_of_items = count_of_unique_items_in_list(copy_of_list)
    sorted_list = sorted(count_of_items, key=lambda x: x[1], reverse=True)
    mode_value = sorted_list[0][0]
    #if the mode is zero return the next highest value as zero signifies missing information
    if mode_value == 0:
        mode_value = sorted_list[1][0]
        
    return mode_value

def calculate_correlation(list_one, list_two):
    """
    A function that takes in two lists and calculates the correlation between them

    Parameters
    ----------
    list_one : list
        A list of values.
    list_two : list
        A list of value.

    Returns
    -------
    correlation_value: float
        The result of the correlation between the two lists provided

    """
    #calculate the mean of both lists
    mean_list_one = calculate_mean(list_one)
    mean_list_two = calculate_mean(list_two)
    
    #create a list of the deviations
    x_deviations = [x - mean_list_one for x in list_one]
    y_deviations = [y - mean_list_two for y in list_two]
    
    #create a list of the deviations multiplied
    xy_deviations = [x*y for (x,y) in zip(x_deviations, y_deviations)]
    
    #create a list of the deviations squared
    x_sqd_deviations = [(x - mean_list_one) ** 2 for x in list_one]
    y_sqd_deviations = [(y - mean_list_two) ** 2 for y in list_two]
    
    #calculate the correlation
    correlation_value = sum(xy_deviations)/(sqrt(sum(x_sqd_deviations))*(sqrt(sum(y_sqd_deviations))))
    
    return correlation_value
    
def main_menu():
    """
    A function for printing out the Main Menu of the program

    Returns
    -------
    None.

    """
    print()
    print("Menu Options:")
    print("-------------")
    print("Enter \"A\" for analysis\nEnter \"H\" for help\nEnter \"Q\" to quit")

def main_menu_error():
    """
    A function for displaying error messages if a user enters an invalid entry on the Main Menu

    Returns
    -------
    None.

    """
    print()
    print("ERROR: Invalid selection. Please enter one of the following options only:")
    print()
    print("\"A\" - for analysis of book data")
    print("\"H\" - for help and information")
    print("\"Q\" - to quit")
    
def quit_message():
    """
    A function for displaying a message to the user when they decide to quit the application

    Returns
    -------
    None.

    """
    print()
    print("Closing application, goodbye!")

def help_section_info():
    """
    A function to display information if the user selects the Help option on the Main Menu

    Returns
    -------
    None.

    """
    print()
    print("***HELP SECTION***")
    print("==================")
    print("This program analyses a file containing almost 7000 books taken from the following dataset on kaggle:")
    print()
    print("https://www.kaggle.com/dylanjcastillo/7k-books-with-metadata")
    print()
    print("If you enter \"A\" on the main menu, a list of analysis options will be displayed.")
    print()
    print("These options include the following:")
    print()
    print("1. Book Information")
    print("   - Details of the number of books and pages on file")
    print("   - Details of the number of book reviews in the file")
    print("   - Details of the averge ratings for books in the file")
    print("   - Details of the years books in the file were published")
    print()
    print("2. Statistical Analysis")
    print("   - The mean, mode, median and standard deviation of book page numbers")
    print("   - The mean, mode, median and standard deviation of average reviews")
    print("   - The mean, mode, median and standard deviation of number of reviews")
    print("   - Correlation information for page numbers and average rating")
    print()
    print("3. Additional Analysis")
    print("   - Title information on the longest book")
    print("   - Title information on the shortest book")
    print("   - List of books with the same number of pages as the mean")
    print("   - List of top ten longest books on file")
    print()
    print("4. Visualizations") 
    print("   - Various visualizations showing results of analysis")
    print("   - Output includes bar charts, pie charts and scatter plots")
    print()
    print("5. Save to File")
    print("   - The option to save output to a text file")
    print()

def analysis_menu():
    """
    A function to display the Analysis Menu options

    Returns
    -------
    None.

    """
    print()
    print("Menu Options:")
    print("-------------")
    print("Enter \"B\" for book page information\nEnter \"S\" for statistical analysis\nEnter \"A\" for additional analysis\nEnter \"V\" for visualizations\nEnter \"F\" to save results to a file\nEnter \"M\" to return to main menu")

def analysis_error_menu():
    """
    A function to display the options on the Analysis Menu

    Returns
    -------
    None.

    """
    print("ERROR: Invalid selection. Please enter one of the following options only:")
    print()
    print("\"B\" - for book information")
    print("\"S\" - for statistical analysis")
    print("\"A\" - for additional analysis")
    print("\"V\" - for visualizations")
    print("\"F\" - to save results to a file")
    print("\"M\" - to return to the main menu")
    print()
    
def book_information_menu(list_of_book_pages, list_of_number_of_ratings, list_of_years):
    """
    A function to display the output of the Book information option on the Analysis Menu

    Parameters
    ----------
    list_of_book_pages : list
        A list of page numbers per book
    list_of_number_of_ratings : list
        A list of the number of ratings per book
    list_of_years : list
        A list of the number of the published year for each book

    Returns
    -------
    None.

    """
    print("Book Information:")
    print("-----------------")
    print()
    print("Books and Pages:")
    print("1. Total number of books in list:", get_total_number_of_records_in_list(list_of_book_pages))
    print("2. Total pages in all books combined:", int(sum(list_of_book_pages)))
    print()
    print("Page Numbers:")
    print("1. Most pages in a book:", get_max_value(list_of_book_pages), "pages")
    print("2. Fewest pages in a book:", get_fewest_pages_excluding_zero(list_of_book_pages), "pages")
    print("3. Number of books in file with no page count:", get_number_of_items_with_missing_information(list_of_book_pages))
    print()
    print("Published Year:")
    print("1. Number of unique years a book was published:", len(count_of_unique_items_in_list(list_of_years)))
    print("2. The most recent year a book was published:", get_most_recent_year(list_of_years))
    print("3. The oldest year a book was published:", min(list_of_years))
    print()
    print("Number of Ratings:")
    print("1. Total number of book reviews:", int(sum(list_of_number_of_ratings)))
    print("2. Number of books on file with no reviews:", get_number_of_items_with_missing_information(list_of_number_of_ratings))
    
def visualizations_message():
    """
    A function to display a message to the user when the analysis is running

    Returns
    -------
    None.

    """
    print("Visualizations:")
    print("---------------")
    print()
    print("***LOADING VISUALIZATIONS...***")
    print("- If using Spyder, please check the Plots section to view the visualizations")
    print("- The visualizations are also saved as .png files in the current folder")

def statistical_analysis_info(list_of_book_pages, list_of_average_ratings, list_of_number_of_ratings):
    """
    A function to display the output of the Statistical Analysis option on the Analysis menu

    Parameters
    ----------
    list_of_book_pages : list
        A list of book page numbers.
    list_of_average_ratings : list
        A list of average ratings per books.
    list_of_number_of_ratings : list
        A list of the number of ratings per book.

    Returns
    -------
    None.

    """
    print("Mean, Mode, Median & Standard Deviation:")
    print("----------------------------------------")
    print()
    print("Statistics for Page Numbers per Book:")
    print("1.1. Mean number of pages per book:", int(round(calculate_mean(list_of_book_pages), 0)))
    print("1.2. Standard deviation of book pages:", int(calculate_standard_deviation(list_of_book_pages)))
    print("1.3. Mode of book pages:", int(calculate_mode(list_of_book_pages)))
    print("1.4. Median number of book pages:", int(calculate_median(list_of_book_pages)))
    print()
    print("Statistics for Average Rating out of 5 per Book:")
    print("2.1. Mean average rating for all books:", round(calculate_mean(list_of_average_ratings), 2))
    print("2.2. Standard deviation of average ratings:", round(calculate_standard_deviation(list_of_average_ratings), 2))
    print("2.3. Mode of average ratings:", calculate_mode(list_of_average_ratings))
    print("2.4. Median average rating:", round(calculate_median(list_of_average_ratings), 2))
    print()
    print("Statistics for Number of Ratings per Book:") 
    print("3.1. Mean number of ratings per book:", int(calculate_mean(list_of_number_of_ratings)))
    print("3.2. Standard deviation of ratings per book:", int(calculate_standard_deviation(list_of_number_of_ratings)))
    print("3.3. Mode of ratings per book:", int(calculate_mode(list_of_number_of_ratings)))
    print("3.4. Median number ratings per book:", int(calculate_median(list_of_number_of_ratings)))
    print()
    print("Correlation between Number of Pages and Average Rating:")
    print("4.1 Correlation between number of pages and average rating:", round(calculate_correlation(list_of_book_pages, list_of_average_ratings), 2))
    print("    - This suggests a weak positive correlation")
    
def additional_analysis_info(list_of_book_pages, list_of_average_ratings, title_and_pages):
    print("Additional Analysis:")
    print("--------------------")
    print("1. Book with most pages:")
    print("   - ", get_book_with_most_pages(title_and_pages))
    print()
    print("2. Book with fewest pages:")
    print("   - ", get_book_with_fewest_pages(title_and_pages))
    print()
    print("3. Titles with the same number of pages as the mean:")
    get_books_with_same_number_pages_as_mean(list_of_book_pages, title_and_pages)
    print()
    print("4. Top 10 longest books:")
    top_ten_books = get_top_ten_longest_books(title_and_pages)
    print(f"    {' Pages':>5}{'Title':>10}")
    #loop through the top ten longest books and print out the title and number of pages
    for k, v in top_ten_books.items():
        print("   - ", v, "   ", k)
    
if __name__ == "__main__":
    #INTERACTIVE MAIN MENU
    print("***Welcome to the 7kBooks Analysis Program***")
    print("=============================================")
    #loop to keep asking the user to enter selections until they decide to quit
    while True:
        main_menu()
        selection = input("Enter your selection: ")
        #check that the user only inputs a valid selection
        if selection.lower() not in ("a", "h", "q"):
            main_menu_error()
        #close the application if q is entered     
        elif selection.lower() == "q":
            quit_message()
            break
        #display help section if h is entered
        elif selection.lower() == "h":
            help_section_info()
        else:
            print()
            print("Initializing data for analysis...please wait...")
            try:
                #open the book file
                page_numbers, years, average_ratings, number_of_ratings, title_and_page_numbers = get_data("7kBooks.csv")
                while True:
                    print() 
                    print("***ANALYSIS SECTION***")
                    print("======================")
                    analysis_menu() 
                    choice = input("Enter your selection: ").lower()
                    print()
                    #alert users to invalid input
                    if choice not in ("b", "s", "a", "v", "f", "m"):
                        analysis_error_menu()
                    #print out information about the number of pages in the books in the file
                    if choice == "b":
                        book_information_menu(page_numbers, number_of_ratings, years)
                    #display visualizations    
                    if choice == "v":
                        visualizations_message()
                        display_published_years(years)
                        display_visual_page_number_statistics(page_numbers)
                        display_visual_average_rating_statistics(average_ratings)
                        display_visual_number_of_ratings_statistics(number_of_ratings)
                        display_scatter_plot(page_numbers, average_ratings)
                        display_top_ten_longest_books(title_and_page_numbers)
                        
                    #print out reults of statistical analysis calculations on the books in the file
                    elif choice == "s":
                        statistical_analysis_info(page_numbers, average_ratings, number_of_ratings)
                    #print out some additional information on the book titles in the file
                    elif choice == "a":
                        additional_analysis_info(page_numbers, average_ratings, title_and_page_numbers)
                    #save the statistical analysis results to a file
                    elif choice == "f":
                        print("***PRINTING RESULTS...***")
                        print()
                        print("Results can be found in the \"7kBooks_Results.txt\" file in the current folder")
                        print()
                        try:
                            with open("7kBooks_Results.txt", "w") as results_file:
                                results_file.write("          Statistical Analysis Results")
                                results_file.write("\n")
                                results_file.write("================================================")
                                results_file.write("\n")
                                results_file.write("\n")
                                results_file.write("Book Page Number Statistics:")
                                results_file.write("\n")
                                results_file.write("============================")
                                results_file.write("\n")
                                results_file.write("Mean of book pages: ")
                                results_file.write(str(int(calculate_mean(page_numbers))))
                                results_file.write("\n")
                                results_file.write("Mode of book pages: ")
                                results_file.write(str(int(calculate_mode(page_numbers))))
                                results_file.write("\n")
                                results_file.write("Median of book pages: ")
                                results_file.write(str(int(calculate_median(page_numbers))))
                                results_file.write("\n")
                                results_file.write("Standard Deviation of book pages: ")
                                results_file.write(str(int(calculate_standard_deviation(page_numbers))))
                                results_file.write("\n")
                                results_file.write("------------------------------------------------")
                                results_file.write("\n")
                                results_file.write("\n")
                                results_file.write("Book Average Rating Statistics:")
                                results_file.write("\n")
                                results_file.write("===============================")
                                results_file.write("\n")
                                results_file.write("Mean of average rating: ")
                                results_file.write(str(round(calculate_mean(average_ratings), 2)))
                                results_file.write("\n")
                                results_file.write("Mode of average rating: ")
                                results_file.write(str(round(calculate_mode(average_ratings), 2)))
                                results_file.write("\n")
                                results_file.write("Median of average rating: ")
                                results_file.write(str(round(calculate_median(average_ratings), 2)))
                                results_file.write("\n")
                                results_file.write("Standard Deviation of average rating: ")
                                results_file.write(str(round(calculate_standard_deviation(average_ratings), 2)))
                                results_file.write("\n")
                                results_file.write("------------------------------------------------")
                                results_file.write("\n")
                                results_file.write("\n")
                                results_file.write("Book Number of Ratings Statistics:")
                                results_file.write("\n")
                                results_file.write("==================================")
                                results_file.write("\n")
                                results_file.write("Mean of number of ratings: ")
                                results_file.write(str(int(calculate_mean(number_of_ratings))))
                                results_file.write("\n")
                                results_file.write("Mode of number of ratings: ")
                                results_file.write(str(int(calculate_mode(number_of_ratings))))
                                results_file.write("\n")
                                results_file.write("Median of number of ratings: ")
                                results_file.write(str(int(calculate_median(number_of_ratings))))
                                results_file.write("\n")
                                results_file.write("Standard Deviation of number of ratings: ")
                                results_file.write(str(int(calculate_standard_deviation(number_of_ratings))))
                                results_file.write("\n")
                                results_file.write("------------------------------------------------")
                                results_file.write("\n")
                                results_file.write("The original source file can be found here:")
                                results_file.write("\n")
                                results_file.write("\n")
                                results_file.write("https://www.kaggle.com/dylanjcastillo/7k-books-with-metadata")
                        #handle errors when trying to write to the results file
                        except FileNotFoundError:
                            print()
                            print("ERROR: File not found. Please ensure the correct file is being used.")
                        except IsADirectoryError:
                            print()
                            print("ERROR: The name entered is a directory. Please ensure a valid file is entered")
                        except PermissionError:
                            print()
                            print("ERROR: Permission denied. Please ensure the correct file is being used.")                
                    #send user back to the main menu of the program
                    elif choice == "m":
                        print("Returning to main menu...")
                        print()
                        print("***MAIN MENU***")
                        print("===============")
                        break

            #handle errors when trying to read the book file
            except FileNotFoundError:
                print()
                print("ERROR: File not found. Please ensure the correct file is being used.")
            except IsADirectoryError:
                print()
                print("ERROR: The name entered is a directory. Please ensure a valid file is entered")
            except PermissionError:
                print()
                print("ERROR: Permission denied. Please ensure the correct file is being used.")
                
                