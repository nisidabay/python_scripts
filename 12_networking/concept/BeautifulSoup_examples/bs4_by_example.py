#!/usr/bin/python3
from bs4 import BeautifulSoup
from rich.console import Console

console = Console()


def print_(text: str, width: int = 50) -> None:
    text = f"{text}".center(width)
    console.print(text, style="bold green")


html_doc = """
<html><head><title>The Dormouse's story</title></head>
<body>
<a><b>text1</b><c>text2</c></a>
<p class="title"><b>The Dormouse's story</b></p>
<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>

<p class="story">...</p>
"""

soup = BeautifulSoup(html_doc, "lxml")

# Navigating using tag names
print_("This is the head")
print({soup.head})
print_("This is the title")
print("soup.title")
print_("This is the b tag")
print("soup.body.b")
print_("This is the first href tag")
print(soup.body.a)
print_("This is the string of the first ref tag")
print(soup.find('a').string)
print_("This is the text of the first ref tag")
print(soup.find('a').text)
print_("These are all href tag")
print(soup.find_all('a'))

# .contents
# A tag's DIRECT children are available in a list called .contents
print_("These are the contents of head")
print(soup.head.contents)

# ===================================================================
# A string doesn't have contents, because it can't contain anything
# ===================================================================

# .children
# Instead you can iterate over a tag's DIRECT children using .children generator

print_("These are the children of head")
for child in soup.head.children:
    print(child)

# .descendants
# Iterates over direct children, the children of its children and so on.
print_("These are the descendants of head")
for child in soup.head.descendants:
    print(child)

# .string
print_("string of p class")
print(soup.p.string)
# String of the tags, if there are more than one return None
print_("string of html")
print(soup.html.string)

# Iterate over the strings ot the document
print_("Iterating over all the strings in the soup")
for string in soup.strings:
    print(repr(string))

# Iterate over the strings ot the document remove extra whitespace
print_(
    "Iterating over all the strings in the soup removing extra espaces".center(
        50))
for string in soup.stripped_strings:
    print(repr(string))

# .parent
# Every tag and every string has a parent that contains them
print_("This is the title")
title_tag = soup.title
print(title_tag)

title_tag = soup.title
print_("The parent of title")
print(title_tag.parent)

print_("The parent of string")
print(title_tag.string.parent)

print_("The parent of html is the BeautifulSoup object")
html_tag = soup.html
print(type(html_tag.parent))

print_("The parent of BeautifulSoup object is define as None")
print(soup.parent)

# .parents
# Iterate over all of an element's parent
print_("All parents of a")
a_tag = soup.a
for parent in a_tag.parents:
    if parent is None:
        print("This is the only parent")
    else:
        print(parent.name)

# siblings
# Tags that are direct children of the same tag
# =========================================================================
# The next sibling of an only tag is the comma and newline that separates
# =========================================================================
# the tag from the second tag
print_("children of a")
a_tag = soup.a

for child in a_tag.children:
    print(child)

print_("b.next_sibling")
b_tag = soup.b
print(b_tag.next_sibling)

print_("c.previous_sibling")
b_tag = soup.c
print(b_tag.previous_sibling)

# Iterate over siblings
print_("Iterate over next_siblings")
for sibling in soup.a.next_siblings:
    print(repr(sibling))

print_("Iterate over previous_siblings")
for sibling in soup.find(id="link3").previous_siblings:
    print(repr(sibling))

# Iterate over elements. The string that was last parsed
print_("Iterater over next_elements")
for ele in soup.find("a", id="link3").next_elements:
    print(ele)

print_("Iterater over previous_elements")
for ele in soup.find("a", id="link3").previous_elements:
    print(ele)

# Filters. Criteria for searching
print_("Filters criteria for searching html tags")
print(soup.find_all('b'))

print(soup.find_all("a", class_="sister"))

print_("Filters criteria for using regexp")
import re
for tag in soup.find_all(re.compile("^b")):
    print(tag.name)

print_("Filter criteria using a list")
print(soup.find_all(["a", "b"]))

print_("Filter criteria using True")
# True. Matches all the tags in the document
for tag in soup.find_all(True):
    print(tag.name)
