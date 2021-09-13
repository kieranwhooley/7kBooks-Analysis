#Program to test functions used in data analysis
print("This program tests functions in assignment part 3 using pytest")
print()

from pytest import approx
from asl_assignment_part3_7kbooks import calculate_mean
from asl_assignment_part3_7kbooks import calculate_standard_deviation
from asl_assignment_part3_7kbooks import calculate_median
from asl_assignment_part3_7kbooks import calculate_mode
from asl_assignment_part3_7kbooks import calculate_correlation
from asl_assignment_part3_7kbooks import convert_list_of_strings_to_floats
from asl_assignment_part3_7kbooks import convert_dictionary_values_to_int_from_string
from asl_assignment_part3_7kbooks import count_of_unique_items_in_list
from asl_assignment_part3_7kbooks import get_max_value
from asl_assignment_part3_7kbooks import get_top_ten_longest_books
from asl_assignment_part3_7kbooks import get_book_with_fewest_pages
from asl_assignment_part3_7kbooks import get_book_with_most_pages
from asl_assignment_part3_7kbooks import get_fewest_pages_excluding_zero
from asl_assignment_part3_7kbooks import get_most_recent_year
from asl_assignment_part3_7kbooks import get_total_number_of_records_in_list
from asl_assignment_part3_7kbooks import get_number_of_items_with_missing_information

#a test dictionary used in multiple tests below
test_dict = {"Book 1": 123, "Book 2": 153, "Book 3": 103, "Book 4": 236, "Book 5": 341, "Book 6": 384,
                 "Book 7": 53, "Book 8": 244, "Book 9": 524, "Book 10": 563, "Book 11": 143, "Book 12": 213,
                 "Book 13": 423, "Book 14": 342, "Book 15": 1123, "Book 16": 97, "Book 17": 653, }

#tests for functions used in calculations
def test_calculate_mean():
    assert calculate_mean([1, 3, 5, 7, 9]) == 5
    assert calculate_mean([2, 4, 6, 8, 10, 13]) == approx((7.166), 0.001)

def test_calculate_standard_deviation():
    assert calculate_standard_deviation([1, 3, 5, 7, 9]) == approx((2.828), 0.001)
    
def test_calculate_median():
    assert calculate_median([1, 2, 3]) == 2
    assert calculate_median([1, 2, 4, 3]) == 2.5
    
def test_calculate_mode():
    assert calculate_mode([23, 67, 54, 54, 90, 6, 32, 54, 1, 2, 3, 67]) == 54

def test_calculate_correlation():
    list_one = [1, 4, 6, 3, 16]
    list_two = [31, 24, 4, 14, 36]
    assert calculate_correlation(list_one, list_two) == approx((0.3785), 0.001)
    
#tests for functions used in processing data
    
def test_convert_dictionary_values_to_int_from_string():
    test_dict = {"Book 1": "247", "Book 2": "123", "Book 3": "354"}
    assert convert_dictionary_values_to_int_from_string(test_dict) == {"Book 1": 247, "Book 2": 123, "Book 3": 354}

def test_convert_list_of_strings_to_floats():
    assert convert_list_of_strings_to_floats(["12.3", "56", "423.2"]) == [12.3, 56.0, 423.2]
    
def test_count_of_unique_items_in_list():
    assert count_of_unique_items_in_list([1, 1, 3, 5, 5, 3, 2, 4, 5, 4]) == [[1, 2], [3, 2], [5, 3], [2, 1], [4, 2]]

#tests for functions specific to getting information on books and titles

def test_get_max_value():
    assert get_max_value([1, 4, 5, 8, 6, 2, 3, 7]) == 8

def test_get_total_number_of_records_in_list():
    assert get_total_number_of_records_in_list([4, 5.4, 6, 3, 5, 7, 38,"test", "text", 2]) == 10

def test_get_fewest_pages_excluding_zero():
    assert get_fewest_pages_excluding_zero([120, 101, 0, 0, 145, 250, 354, 124]) == 101
    
def test_get_most_recent_year():
    assert get_most_recent_year([1990, 1987, 1986, 2019, 2014, 2007, 1965, 1987, 1912]) == 2019

def test_get_top_ten_longest_books():
    assert get_top_ten_longest_books(test_dict) == {"Book 15": 1123, "Book 17": 653, "Book 10": 563, "Book 9": 524,
                                         "Book 13": 423, "Book 6": 384, "Book 14": 342, "Book 5": 341, 
                                         "Book 8": 244, "Book 4": 236}
    
def test_get_book_with_fewest_pages():
    assert get_book_with_fewest_pages(test_dict) == "Book 7"
    
def test_get_book_with_most_pages():
    assert get_book_with_most_pages(test_dict) == "Book 15"
    
def test_get_number_of_items_with_missing_information():
    assert get_number_of_items_with_missing_information([0, 2, 5, 67, 22, 0, 5, 7, 0, 0, 43]) == 4
    

 

    
    

    

