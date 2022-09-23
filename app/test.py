data = {
    'tag': 'WE11',
    'width': 0.150,
    'length': 4.170,
    'height': 3.0,
    'unit': 'm',
    'rebars': {
        'v': {'type': "m12", 'spacing': 0.400},
        'h': {'type': "m10", 'spacing': 0.600},
    },
    'openings': [
        {'tag': 'W101', 'width': 1200, 'height': 900, 'amt': 2},
        {'tag': 'D21', 'width': 950, 'height': 2100, 'amt': 1},

    ]

    
}

openings= [
        {'tag': 'W101', 'width': 1200, 'height': 900, 'amt': 2},
        {'tag': 'D21', 'width': 950, 'height': 2100, 'amt': 1},

    ]

def process_openings(data:list=None, factor:int=None):
    def convert(item ):
        item['height'] = item['height'] / factor
        item['width'] = item['width'] / factor
        return item
    return list(map(convert, data))


print(process_openings(data=data['openings'], factor=1000))