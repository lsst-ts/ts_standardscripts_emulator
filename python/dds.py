#
# Fake enough of dds to allow us to run scriptQueue scripts without DDS or SAL
#
class DomainParticipant:
    def __init__(self, qos):
        self.qos = qos

    def close(self):
        pass

    def create_publisher(self, qos):
        return Publisher(qos)

    def create_subscriber(self, qos):
        return Subscriber(qos)

class DurabilityQosPolicy:
    def __init__(self, policy):
        self.policy = policy

class DDSDurabilityKind:
    class VOLATILE: pass


class DDSDuration:
    def __init__(self, sec=10):
        self.sec = sec

class DDS_READ_QUEUE_LEN: pass


class DDSHistoryKind:
    class KEEP_LAST: pass


class DDSStateKind:
    class NOT_READ_SAMPLE_STATE: pass
    class ALIVE_INSTANCE_STATE: pass

    
class GuardCondition:
    def __init__(self):
        pass

    def trigger(self):
        pass


class HistoryQosPolicy:
    def __init__(self, depth, kind):
        self.depth = depth
        self.kind = kind

class PartitionQosPolicy:
    def __init__(self, partition_names):
        self.names = partition_names

class Publisher:
    def __init__(self, qos):
        self.qos = qos

    def create_datawriter(self, topic, qos):
        return Writer()

        
class _Qos:
    def __init__(self):
        pass

    def set_policies(self, policies):
        self.policies = policies

class QosProvider:
    def __init__(self, qosUri, qosName):
        self.qosUri = qosUri
        self.qosName = qosName
        self.participant_qos = _Qos()
        self.publisher_qos = _Qos()
        self.reader_qos = _Qos()
        self.subscriber_qos = _Qos()
        self.topic_qos = _Qos()
        self.writer_qos = _Qos()

    def get_participant_qos(self):
        return self.participant_qos

    def get_publisher_qos(self):
        return self.publisher_qos

    def get_reader_qos(self):
        return self.reader_qos

    def get_subscriber_qos(self):
        return self.subscriber_qos
    
    def get_topic_qos(self):
        return self.topic_qos
    
    def get_writer_qos(self):
        return self.writer_qos


class QueryCondition:
    def __init__(self, _reader, read_mask, full_query):
        pass


class Reader:
    def __init__(self):
        pass

    def create_readcondition(self, read_mask):
        return None
    
    def close(self):
        pass


class Subscriber:
    def __init__(self, qos):
        self.qos = qos

    def create_datareader(self, topic, qos):
        self.topic = topic
        self.qos = qos

        return Reader()


class WaitSet:
    def __init__(self):
        pass

    def attach(self, guardcond):
        self.guardcond = guardcond

    def wait(self, wait_timeout):
        return []

    
class Writer:
    def __init__(self):
        pass

    def write(self, data):
        pass
