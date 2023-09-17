class LibdbSchema():
    def __init__(self, version, name, description, libraries):
        self.version
        self.name
        self.description
        self.libraries

    def to_dict(self):
        return {
            "meta": {
                "version": self.version
            },
            "name": self.name,
            "description": self.description,
            "libraries": [library.to_dict() for library in self.libraries]
        }