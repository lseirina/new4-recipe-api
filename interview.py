def my_decorator(func):
    def wrapper(*args, **kwargs):
        i = 1
        while i < len(args):
            try:
                result = func(*args, **kwargs)
                return result
            except:
                i += 1
                continue

    return wrapper

@my_decorator
def add_items(*args):
    if args is None:
        return None
    result = args[0]

    for arg in args[1:]:
        result += arg

    return result

print(add_items('Hello', 1))


# def add_items(*args):
#     if args is None:
#         return None
#     result = args[0]
#     for arg in args[1:]:
#         if isinstance(result, (int, float)) and isinstance(arg, (int, float)):
#             result += arg
#         else:
#             try:
#                 result = str(result) + str(arg)
#             except Exception as e:
#                 print(f'Error for combining {result} and {arg}: {e}')

#     return result

# print(add_items('Hello ', 1, 4))