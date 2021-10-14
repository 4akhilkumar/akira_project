from django import template
register = template.Library()

@register.filter
def first_letter_word(value):
    lst = value.split(" ")
    chindex=1
    arr = []
    if "and" in lst:
        lst.remove("and")
    for letter in lst:
        if chindex==1:
            arr.append(letter[0].upper().strip("&"))
        else:
            arr.append(letter)
    out = "".join(arr)
    return out