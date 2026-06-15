from sqlalchemy.orm import Session
from models.swimlane import Swimlane


class SwimlaneRepository:

    def __init__(self, db: Session):
        self.db = db

    def create_swimlane(
        self,
        board_id: int,
        name: str,
        position: int = 0
    ) -> Swimlane:

        lane = Swimlane(
            board_id=board_id,
            name=name,
            position=position
        )

        self.db.add(lane)
        self.db.commit()
        self.db.refresh(lane)

        return lane

    def get_by_id(self, lane_id: int):
        return self.db.query(Swimlane).filter(
            Swimlane.id == lane_id
        ).first()

    def get_by_board(self, board_id: int):
        return self.db.query(Swimlane).filter(
            Swimlane.board_id == board_id
        ).order_by(Swimlane.position).all()

    def update_name(self, lane_id: int, new_name: str):
        lane = self.get_by_id(lane_id)

        if lane:
            lane.name = new_name
            self.db.commit()
            self.db.refresh(lane)

        return lane

    def update_position(self, lane_id: int, new_position: int):
        lane = self.get_by_id(lane_id)

        if lane:
            lane.position = new_position
            self.db.commit()
            self.db.refresh(lane)

        return lane

    def delete_swimlane(self, lane_id: int):
        lane = self.get_by_id(lane_id)

        if lane:
            self.db.delete(lane)
            self.db.commit()
            return True

        return False