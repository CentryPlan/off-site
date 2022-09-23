#Webs App

class BlockWall:
    ''' A Concrete Masonry Unit . Accepts only Feet and Meters '''
    tracker:list = []
    data_flag:bool = False 

    def __init__(self, data:dict=None):
        if data:
            self.data_flag = True  
            self.tag = data.get('tag')                   
            self.width = data.get('width')
            self.length = data.get('length')
            self.height = data.get('height')
            self.rebars = data.get('rebars')
            self.openings = data.get('openings', [])
            self.unit = self.set_units(unit=data.get('unit'))             
            self.process_data  
            self.track_wall    
            self.process_rebar


    @property
    def area(self):
        if self.data_flag:
            return {
                "unit": self.unit.get('area'), 
                "value": round((self.length['value'] * self.height['value']) - sum(self.openings.get('areas')),2)
                }
        return None

    @property
    def blocks(self):
        if self.unit['len'] == 'ft':
            block_area = .667 *1.333
        else:
            block_area = 0.2 * 0.4
        return {'unit': 'Each', 'value': round(self.area['value'] / block_area) + 1}

    #------------- Data Processors ---------------- 

    def set_units(self, unit:str=None):
        '''Process wall units'''
        data = { "len": "", "area": "", "vol": ""}
        factor = 1
        if unit == 'm': # Case m needs no conversion             
            data['len'] = 'm'; data['area'] = 'm2'; data['vol'] = 'm3'
            self.process_measurements(factor)
            self.openings = self.process_openings(data = self.openings, factor=factor)
           
        if unit == 'mm': # Case mm convert to m 
            factor = 1000
            data['len'] = 'm'; data['area'] = 'm2'; data['vol'] = 'm3'
            self.process_measurements(factor)
            self.openings = self.process_openings(data = self.openings, factor=factor)
        if unit == 'ft': # Case ft needs no conversion            
            data['len'] = 'ft'; data['area'] = 'ft2'; data['vol'] = 'ft3'                       
        return data

    def process_measurements(self, factor):
        # Convert Measurements
        self.width = self.width/factor
        self.length = self.length/factor
        self.height = self.height/factor

    @property
    def process_data(self):
        self.width = {"unit": self.unit.get('len'),  "value": self.width}
        self.length = {"unit": self.unit.get('len'),  "value": self.length}
        self.height = {"unit": self.unit.get('len'),  "value": self.height}
    
    def process_openings(self, data:list=None, factor:int=None):
        def convert(item ):
            item['height'] = item['height'] / factor
            item['width'] = item['width'] / factor            
            return item
        def areas(item):
            return round((item['width'] * item['height']) * item['amt'], 2)
        def jamb(item):
            if 'D' in item.get('tag'):
                return round((item['width'] + (2 * item['height'])) * item['amt'],2) # Doors
            else:
                return round(((item['width'] * 2) + (2 * item['height'])) * item['amt'], 2)# Windows
        return {
            'openings': list(map(convert, data)),
            'areas': list(map(areas, data)),
            'jamb': list(map(jamb, data)),
        }

    @property
    def process_rebar(self):
        self.rebars['h']['amt'] = round((self.height['value'] / self.rebars['h']['spacing'])) +1            
        self.rebars['v']['amt'] = round((self.length['value'] / self.rebars['v']['spacing'])) + 1
        
        self.rebars['h']['bars'] = round(((self.rebars['h']['amt'] * self.length['value'])) / 9)
        self.rebars['v']['bars'] = round(((self.rebars['v']['amt'] * self.height['value'])) / 9)
        print(self.rebars)

    # Trackers
    @property
    def track_wall(self):
        if self.data_flag:
            self.tracker.append({
                'tag': self.tag,
                'length': self.length,
                'width':self.width,
                'area': self.area
            })
    
    @property
    def wall_segments(self): return len(self.tracker)

    @property
    def wall_ids(self): 
        def id_tag(item):
            return item['tag']
        return list(map(id_tag, self.tracker))
        

        

# Execute Program
data = {
    'tag': 'WE11',
    'width': .150,
    'length': 4.170,
    'height': 3.000,
    'unit': 'm',
    'rebars': {
        'v': {'type': "m12", 'spacing': 0.400},
        'h': {'type': "m10", 'spacing': 0.600},
    },
    'openings': [
        {'tag': 'W101', 'width': 1.200, 'height': .900, 'amt': 1},
        {'tag': 'D21', 'width': .950, 'height': 2.100, 'amt': 3},
    ]

    
}
wall = BlockWall(data=data)
data['tag'] = 'WS15'
data['height'] = 6.000
data['length'] = 10.000
wall3 = BlockWall(data=data)

#print(wall.blocks)
#print(wall.area)
#print(wall.openings)