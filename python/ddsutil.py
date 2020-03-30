#
# Fake enough of dds to allow us to run scriptQueue scripts without DDS or SAL
#
class DataType:
    def __init__(self):
        
        self.classname = 'rhl'
        self.description = 'xxx'
        self.filePath = None
        self.functionName = None
        self.level = None
        self.lineNumber = None
        self.message = 'yyy'
        self.process = None
        self.traceback = None

class Topic:
    def __init__(self):
        self.topic_data_class = DataType

    def register_topic(self, participant, dds_name, qos):
        return None

    def write(self, data):
        pass


def get_dds_classes_from_idl(idl_path, ackcmd_revname):
    return Topic()

