from sqlalchemy import create_engine, Column, Integer, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class TrainingData(Base):
    """Training data table with 4 functions"""
    __tablename__ = 'training_data'
    
    id = Column(Integer, primary_key=True)
    x = Column(Float, nullable=False, unique=True)
    y1 = Column(Float, nullable=False)
    y2 = Column(Float, nullable=False)
    y3 = Column(Float, nullable=False)
    y4 = Column(Float, nullable=False)


class IdealFunctions(Base):
    """Ideal functions table with 50 functions"""
    __tablename__ = 'ideal_functions'
    
    id = Column(Integer, primary_key=True)
    x = Column(Float, nullable=False, unique=True)
    y1 = Column(Float, nullable=False)
    y2 = Column(Float, nullable=False)
    y3 = Column(Float, nullable=False)
    y4 = Column(Float, nullable=False)
    y5 = Column(Float, nullable=False)
    y6 = Column(Float, nullable=False)
    y7 = Column(Float, nullable=False)
    y8 = Column(Float, nullable=False)
    y9 = Column(Float, nullable=False)
    y10 = Column(Float, nullable=False)
    y11 = Column(Float, nullable=False)
    y12 = Column(Float, nullable=False)
    y13 = Column(Float, nullable=False)
    y14 = Column(Float, nullable=False)
    y15 = Column(Float, nullable=False)
    y16 = Column(Float, nullable=False)
    y17 = Column(Float, nullable=False)
    y18 = Column(Float, nullable=False)
    y19 = Column(Float, nullable=False)
    y20 = Column(Float, nullable=False)
    y21 = Column(Float, nullable=False)
    y22 = Column(Float, nullable=False)
    y23 = Column(Float, nullable=False)
    y24 = Column(Float, nullable=False)
    y25 = Column(Float, nullable=False)
    y26 = Column(Float, nullable=False)
    y27 = Column(Float, nullable=False)
    y28 = Column(Float, nullable=False)
    y29 = Column(Float, nullable=False)
    y30 = Column(Float, nullable=False)
    y31 = Column(Float, nullable=False)
    y32 = Column(Float, nullable=False)
    y33 = Column(Float, nullable=False)
    y34 = Column(Float, nullable=False)
    y35 = Column(Float, nullable=False)
    y36 = Column(Float, nullable=False)
    y37 = Column(Float, nullable=False)
    y38 = Column(Float, nullable=False)
    y39 = Column(Float, nullable=False)
    y40 = Column(Float, nullable=False)
    y41 = Column(Float, nullable=False)
    y42 = Column(Float, nullable=False)
    y43 = Column(Float, nullable=False)
    y44 = Column(Float, nullable=False)
    y45 = Column(Float, nullable=False)
    y46 = Column(Float, nullable=False)
    y47 = Column(Float, nullable=False)
    y48 = Column(Float, nullable=False)
    y49 = Column(Float, nullable=False)
    y50 = Column(Float, nullable=False)


class TestResults(Base):
    """Test results table with mapping and deviations"""
    __tablename__ = 'test_results'
    
    id = Column(Integer, primary_key=True)
    x = Column(Float, nullable=False)
    y = Column(Float, nullable=False)
    delta_y = Column(Float, nullable=False)
    ideal_func_num = Column(Integer, nullable=False)


def setup_database(db_name='sqlite:///mapped_data.db'):
    """
    Create database and tables
    """
    engine = create_engine(db_name, echo=False)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return engine, Session()


def populate_database(session, train_df, ideal_df):
    """
    Load training and ideal data into database
    """
    try:
        session.query(TrainingData).delete()
        session.query(IdealFunctions).delete()
        session.query(TestResults).delete()
        session.commit()
        
        for _, row in train_df.iterrows():
            record = TrainingData(
                x=float(row['x']),
                y1=float(row['y1']),
                y2=float(row['y2']),
                y3=float(row['y3']),
                y4=float(row['y4'])
            )
            session.add(record)
        
        for _, row in ideal_df.iterrows():
            kwargs = {'x': float(row['x'])}
            for i in range(1, 51):
                col_name = f'y{i}'
                if col_name in row:
                    kwargs[col_name] = float(row[col_name])
            record = IdealFunctions(**kwargs)
            session.add(record)
        
        session.commit()
        print(f"Loaded {len(train_df)} training records and {len(ideal_df)} ideal records")
        
    except Exception as e:
        session.rollback()
        raise Exception(f"Database population failed: {str(e)}")
