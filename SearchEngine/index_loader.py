# index_loader.py
class IndexLoader:
    @staticmethod
    def load_index(index_file):
        index = {}
        with open(index_file, 'r') as file:
            lines = file.readlines()
            current_word = None
            for line in lines:
                line = line.strip()
                if line:
                    if line.endswith('):'):
                        current_word, df = line.split(' (df: ')
                        df = int(df[:-2])  # Remove trailing '):'
                        index[current_word] = {'df': df, 'positions': {}}
                    else:
                        doc_info = line.split(', Positions: ')
                        doc_id = int(doc_info[0].split(': ')[1])
                        positions = list(map(int, doc_info[1].strip('[]').split(', ')))
                        index[current_word]['positions'][doc_id] = positions
        return index
