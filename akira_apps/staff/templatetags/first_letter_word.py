from django import template
register = template.Library()

@register.filter
def first_letter_word(value):
    value.split(" ")
    chindex=1
    arr = []
    for letter in value.split(" "):
        if chindex==1:
            arr.append(letter[0].upper())
        else:
            arr.append(letter)
    out = "".join(arr)
    return out