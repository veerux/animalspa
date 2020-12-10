service_list = []


def get_last_id():
    if service_list:
        last_service = service_list[-1]
    else:
        return 1
    return last_service.id + 1


class Service:
    def __init__(self, name, description, duration):
        self.id = get_last_id()
        self.name = name
        self.description = description
        self.duration = duration

    @property
    def data(self):
        return {'id': self.id, 'name': self.name, 'description': self.description, 'duration': self.duration}
