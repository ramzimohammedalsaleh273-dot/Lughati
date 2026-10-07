from datetime import datetime
from sqlalchemy import String, Integer, Float, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

class Child(Base):
    __tablename__="children"
    id: Mapped[int]=mapped_column(primary_key=True)
    name: Mapped[str]=mapped_column(String(100))
    age: Mapped[int]=mapped_column(Integer, default=6)
    created_at: Mapped[datetime]=mapped_column(DateTime, default=datetime.utcnow)
    progress: Mapped[list["Progress"]]=relationship(back_populates="child", cascade="all, delete-orphan")

class Lesson(Base):
    __tablename__="lessons"
    id: Mapped[int]=mapped_column(primary_key=True)
    language: Mapped[str]=mapped_column(String(10))
    level: Mapped[int]=mapped_column(Integer)
    title: Mapped[str]=mapped_column(String(200))
    skill: Mapped[str]=mapped_column(String(50))
    body: Mapped[str]=mapped_column(Text, default="")
    audio: Mapped[str|None]=mapped_column(String(500), nullable=True)
    video: Mapped[str|None]=mapped_column(String(500), nullable=True)

class Word(Base):
    __tablename__="words"
    id: Mapped[int]=mapped_column(primary_key=True)
    language: Mapped[str]=mapped_column(String(10))
    text: Mapped[str]=mapped_column(String(100))
    meaning: Mapped[str]=mapped_column(String(200), default="")
    example: Mapped[str]=mapped_column(String(300), default="")
    level: Mapped[int]=mapped_column(Integer, default=0)

class Progress(Base):
    __tablename__="progress"
    id: Mapped[int]=mapped_column(primary_key=True)
    child_id: Mapped[int]=mapped_column(ForeignKey("children.id"))
    lesson_id: Mapped[int]=mapped_column(ForeignKey("lessons.id"))
    score: Mapped[float]=mapped_column(Float, default=0)
    mastered: Mapped[bool]=mapped_column(Boolean, default=False)
    updated_at: Mapped[datetime]=mapped_column(DateTime, default=datetime.utcnow)
    child: Mapped["Child"]=relationship(back_populates="progress")

class TestResult(Base):
    __tablename__="test_results"
    id: Mapped[int]=mapped_column(primary_key=True)
    child_id: Mapped[int]=mapped_column(ForeignKey("children.id"))
    language: Mapped[str]=mapped_column(String(10))
    skill: Mapped[str]=mapped_column(String(50))
    score: Mapped[float]=mapped_column(Float)
    created_at: Mapped[datetime]=mapped_column(DateTime, default=datetime.utcnow)

class ReviewItem(Base):
    __tablename__="review_items"
    id: Mapped[int]=mapped_column(primary_key=True)
    child_id: Mapped[int]=mapped_column(ForeignKey("children.id"))
    word_id: Mapped[int]=mapped_column(ForeignKey("words.id"))
    state: Mapped[str]=mapped_column(String(30), default="new")
    ease: Mapped[float]=mapped_column(Float, default=2.5)
    repetitions: Mapped[int]=mapped_column(Integer, default=0)
    next_review: Mapped[datetime]=mapped_column(DateTime, default=datetime.utcnow)
