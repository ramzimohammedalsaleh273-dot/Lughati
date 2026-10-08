from datetime import datetime
from sqlalchemy import String,Integer,Float,Boolean,DateTime,ForeignKey,Text
from sqlalchemy.orm import Mapped,mapped_column,relationship
from app.database import Base

class Child(Base):
    __tablename__="children"; id:Mapped[int]=mapped_column(primary_key=True); name:Mapped[str]=mapped_column(String(100)); age:Mapped[int]=mapped_column(Integer,default=6); created_at:Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow); progress:Mapped[list["Progress"]]=relationship(back_populates="child",cascade="all, delete-orphan")
class Lesson(Base):
    __tablename__="lessons"; id:Mapped[int]=mapped_column(primary_key=True); language:Mapped[str]=mapped_column(String(10)); level:Mapped[int]=mapped_column(Integer); title:Mapped[str]=mapped_column(String(200)); skill:Mapped[str]=mapped_column(String(50)); body:Mapped[str]=mapped_column(Text,default=""); audio:Mapped[str|None]=mapped_column(String(500),nullable=True); video:Mapped[str|None]=mapped_column(String(500),nullable=True)
class Word(Base):
    __tablename__="words"; id:Mapped[int]=mapped_column(primary_key=True); language:Mapped[str]=mapped_column(String(10)); text:Mapped[str]=mapped_column(String(100)); meaning:Mapped[str]=mapped_column(String(200),default=""); example:Mapped[str]=mapped_column(String(300),default=""); level:Mapped[int]=mapped_column(Integer,default=0)
class Progress(Base):
    __tablename__="progress"; id:Mapped[int]=mapped_column(primary_key=True); child_id:Mapped[int]=mapped_column(ForeignKey("children.id")); lesson_id:Mapped[int]=mapped_column(ForeignKey("lessons.id")); score:Mapped[float]=mapped_column(Float,default=0); mastered:Mapped[bool]=mapped_column(Boolean,default=False); updated_at:Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow); child:Mapped["Child"]=relationship(back_populates="progress")
class TestResult(Base):
    __tablename__="test_results"; id:Mapped[int]=mapped_column(primary_key=True); child_id:Mapped[int]=mapped_column(ForeignKey("children.id")); language:Mapped[str]=mapped_column(String(10)); skill:Mapped[str]=mapped_column(String(50)); score:Mapped[float]=mapped_column(Float); created_at:Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow)
class ReviewItem(Base):
    __tablename__="review_items"; id:Mapped[int]=mapped_column(primary_key=True); child_id:Mapped[int]=mapped_column(ForeignKey("children.id")); word_id:Mapped[int]=mapped_column(ForeignKey("words.id")); state:Mapped[str]=mapped_column(String(30),default="new"); ease:Mapped[float]=mapped_column(Float,default=2.5); repetitions:Mapped[int]=mapped_column(Integer,default=0); next_review:Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow)
class Story(Base):
    __tablename__="stories"; id:Mapped[int]=mapped_column(primary_key=True); language:Mapped[str]=mapped_column(String(10)); level:Mapped[int]=mapped_column(Integer,default=0); title:Mapped[str]=mapped_column(String(200)); body:Mapped[str]=mapped_column(Text,default=""); questions:Mapped[str]=mapped_column(Text,default="[]")
class Question(Base):
    __tablename__="questions"; id:Mapped[int]=mapped_column(primary_key=True); language:Mapped[str]=mapped_column(String(10)); level:Mapped[int]=mapped_column(Integer,default=0); skill:Mapped[str]=mapped_column(String(50)); prompt:Mapped[str]=mapped_column(Text); options:Mapped[str]=mapped_column(Text,default="[]"); answer:Mapped[str]=mapped_column(Text)
class Achievement(Base):
    __tablename__="achievements"; id:Mapped[int]=mapped_column(primary_key=True); code:Mapped[str]=mapped_column(String(80),unique=True); title:Mapped[str]=mapped_column(String(200)); description:Mapped[str]=mapped_column(Text,default="")
class ChildAchievement(Base):
    __tablename__="child_achievements"; id:Mapped[int]=mapped_column(primary_key=True); child_id:Mapped[int]=mapped_column(ForeignKey("children.id")); achievement_id:Mapped[int]=mapped_column(ForeignKey("achievements.id")); earned_at:Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow)
class DailyPlan(Base):
    __tablename__="daily_plans"; id:Mapped[int]=mapped_column(primary_key=True); child_id:Mapped[int]=mapped_column(ForeignKey("children.id")); date:Mapped[str]=mapped_column(String(10)); language:Mapped[str]=mapped_column(String(10)); minutes:Mapped[int]=mapped_column(Integer,default=20); completed:Mapped[bool]=mapped_column(Boolean,default=False); tasks:Mapped[str]=mapped_column(Text,default="[]")
class Activity(Base):
    __tablename__="activities"; id:Mapped[int]=mapped_column(primary_key=True); lesson_id:Mapped[int]=mapped_column(ForeignKey("lessons.id")); kind:Mapped[str]=mapped_column(String(40)); instruction:Mapped[str]=mapped_column(Text); content:Mapped[str]=mapped_column(Text,default=""); order_no:Mapped[int]=mapped_column(Integer,default=0)
class MediaAsset(Base):
    __tablename__="media_assets"; id:Mapped[int]=mapped_column(primary_key=True); language:Mapped[str]=mapped_column(String(10)); level:Mapped[int]=mapped_column(Integer,default=0); kind:Mapped[str]=mapped_column(String(30)); title:Mapped[str]=mapped_column(String(200)); path:Mapped[str]=mapped_column(String(1000),default=""); source:Mapped[str]=mapped_column(String(500),default=""); offline_ready:Mapped[bool]=mapped_column(Boolean,default=False)
class AssessmentAttempt(Base):
    __tablename__="assessment_attempts"; id:Mapped[int]=mapped_column(primary_key=True); child_id:Mapped[int]=mapped_column(ForeignKey("children.id")); language:Mapped[str]=mapped_column(String(10)); level:Mapped[int]=mapped_column(Integer,default=0); total:Mapped[int]=mapped_column(Integer,default=0); correct:Mapped[int]=mapped_column(Integer,default=0); score:Mapped[float]=mapped_column(Float,default=0); started_at:Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow); finished_at:Mapped[datetime|None]=mapped_column(DateTime,nullable=True)
class Recording(Base):
    __tablename__="recordings"; id:Mapped[int]=mapped_column(primary_key=True); child_id:Mapped[int]=mapped_column(ForeignKey("children.id")); language:Mapped[str]=mapped_column(String(10)); prompt:Mapped[str]=mapped_column(Text,default=""); path:Mapped[str]=mapped_column(String(1000)); duration:Mapped[float]=mapped_column(Float,default=0); self_score:Mapped[int]=mapped_column(Integer,default=0); created_at:Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow)
class ParentProfile(Base):
    __tablename__="parent_profiles"; id:Mapped[int]=mapped_column(primary_key=True); name:Mapped[str]=mapped_column(String(120),default="ولي الأمر"); pin_hash:Mapped[str]=mapped_column(String(255),default=""); created_at:Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow)
class UserSetting(Base):
    __tablename__="user_settings"; id:Mapped[int]=mapped_column(primary_key=True); key:Mapped[str]=mapped_column(String(150),unique=True); value:Mapped[str]=mapped_column(Text,default="")
class SyncEvent(Base):
    __tablename__="sync_events"; id:Mapped[int]=mapped_column(primary_key=True); entity:Mapped[str]=mapped_column(String(80)); entity_id:Mapped[int]=mapped_column(Integer); operation:Mapped[str]=mapped_column(String(20)); payload:Mapped[str]=mapped_column(Text,default="{}"); status:Mapped[str]=mapped_column(String(20),default="pending"); created_at:Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow); synced_at:Mapped[datetime|None]=mapped_column(DateTime,nullable=True)

class CurriculumUnit(Base):
    __tablename__="curriculum_units"
    id:Mapped[int]=mapped_column(primary_key=True)
    language:Mapped[str]=mapped_column(String(10))
    age_group:Mapped[str]=mapped_column(String(20))
    level:Mapped[int]=mapped_column(Integer)
    skill:Mapped[str]=mapped_column(String(50))
    kind:Mapped[str]=mapped_column(String(30),default="lesson")
    title:Mapped[str]=mapped_column(String(250))
    body:Mapped[str]=mapped_column(Text,default="")
    payload:Mapped[str]=mapped_column(Text,default="{}")

class VideoLesson(Base):
    __tablename__="video_lessons"
    id:Mapped[int]=mapped_column(primary_key=True)
    language:Mapped[str]=mapped_column(String(10)); age_group:Mapped[str]=mapped_column(String(20)); level:Mapped[int]=mapped_column(Integer)
    curriculum_unit_id:Mapped[int|None]=mapped_column(ForeignKey("curriculum_units.id"),nullable=True)
    title:Mapped[str]=mapped_column(String(250)); character:Mapped[str]=mapped_column(String(80),default="ليان"); video_path:Mapped[str]=mapped_column(String(1000),default="")
    duration:Mapped[float]=mapped_column(Float,default=0); status:Mapped[str]=mapped_column(String(30),default="script_ready"); manifest:Mapped[str]=mapped_column(Text,default="{}"); license:Mapped[str]=mapped_column(String(100),default="")

class VideoInteraction(Base):
    __tablename__="video_interactions"
    id:Mapped[int]=mapped_column(primary_key=True); video_lesson_id:Mapped[int]=mapped_column(ForeignKey("video_lessons.id")); order_no:Mapped[int]=mapped_column(Integer)
    kind:Mapped[str]=mapped_column(String(40)); prompt:Mapped[str]=mapped_column(Text,default=""); expected:Mapped[str]=mapped_column(Text,default=""); payload:Mapped[str]=mapped_column(Text,default="{}")
