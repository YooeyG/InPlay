print('Imported my module...')

test = 'Test String'

def find_index(to_search, target):
    '''Find the index of a valuein a sequence'''
    for i, value in enumerate(to_search):
        if value == target:
            return i

    return -1