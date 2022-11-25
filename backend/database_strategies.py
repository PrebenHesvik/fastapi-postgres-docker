from fastapi import HTTPException, status, Response


class CommitData:
    def __init__(self, db, data):
        self.db = db
        self.data = data

    def __enter__(self):
        self.db.add(self.data)

    def __exit__(self, exc_type, exc_val, traceback):
        self.db.commit()
        self.db.refresh(self.data)


class UpdataData:
    def __init__(self, db, query, updated_data, identifier, context):
        self.db = db
        self.query = query
        self.updated_data = updated_data
        self.identifier = identifier
        self.context = context
        self.match = self.query.first()

    def validate(self):
        if self.match is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{self.context} with identifier of <{self.identifier}> was not found",
            )

    def run(self):
        self.validate()
        if isinstance(self.updated_data, dict):
            self.query.update(self.updated_data, synchronize_session=False)
        else:
            self.query.update(self.updated_data.dict(), synchronize_session=False)
        self.db.commit()
        return self.query.first()


class DeleteData:
    def __init__(self, db, query, identifier, context):
        self.db = db
        self.query = query
        self.identifier = identifier
        self.context = context
        self.match = self.query.first()

    def validate(self):
        if self.match is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{self.context} with identifier of <{self.identifier}> was not found",
            )

    def run(self):
        self.validate()
        self.query.delete(synchronize_session=False)
        self.db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
