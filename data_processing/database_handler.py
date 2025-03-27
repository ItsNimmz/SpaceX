# models.py
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Date, ForeignKey, Numeric, Float, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

# Base class for all models
Base = declarative_base()

# Rocket Table
class Rocket(Base):
    __tablename__ = 'rocket'

    id = Column(Integer, primary_key=True, autoincrement=True)
    rocket_id = Column(String, unique=True, nullable=False)
    rocket_name = Column(String, nullable=False)
    country = Column(String, nullable=False)
    description = Column(String, nullable=True)
    first_flight = Column(Date, nullable=True)  # Date of first launch
    active = Column(String, nullable=True, default=False)  # Current status
    type = Column(String, nullable=True)  # Rocket type/family
    cost_per_launch = Column(Numeric, nullable=True)
    diameter = Column(Float, nullable=True)  # Diameter in meters
    mass = Column(Float, nullable=True)  # Mass in kilograms
    

    # launches = relationship('launche', backref='rocket', lazy='dynamic')

    def __repr__(self):
        return f"<Rocket(rocket_id={self.rocket_id}, rocket_name={self.rocket_name})>"

# Launch Table
class Launch(Base):
    __tablename__ = 'launches'

    id = Column(Integer, primary_key=True, autoincrement=True)
    mission_id = Column(String, nullable=False)
    mission_name = Column(String, nullable=False)
    launch_date_utc = Column(DateTime, nullable=False)
    details = Column(String, nullable=True)
    rocket_id = Column(Integer, ForeignKey('rocket.id'), nullable=False)
    
    # Relationships
    rocket = relationship('Rocket', backref='launches')

    def __repr__(self):
        return f"<Launch(mission_id={self.mission_id}, mission_name={self.mission_name}, rocket_id={self.rocket_id}, payload_id={self.payload_id})>"

# Function to create tables
def create_tables():
    # Database connection setup
    DATABASE_URL = 'sqlite:///spacexv1.db'  # SQLite for simplicity (can be changed to other DBs)
    engine = create_engine(DATABASE_URL, echo=True)
    Base.metadata.create_all(engine)
    print("Tables created successfully.")

# Function to create a session
def get_session():
    DATABASE_URL = 'sqlite:///spacexv1.db'  # SQLite for simplicity (can be changed to other DBs)
    engine = create_engine(DATABASE_URL, echo=True)
    Session = sessionmaker(bind=engine)
    return Session()


def bulk_insert(df, table_name: str):
        """ Bulk insert data from DataFrame into a specified table. """
        session = get_session()
    
        try:
            # Convert DataFrame to dictionary of rows
            data = df.to_dict(orient='records')
            # Dynamically get the table class from the models
            table_class = globals().get(table_name.capitalize())
            
            if table_class:
                if table_name == 'launch':  # Special handling for 'launch' table
                    
                    # Fetch Rocket IDs and map them to the correct ID
                    for record in data:
                        rocket_id_str = record['rocket_id']
                        rocket = session.query(Rocket).filter(Rocket.rocket_id == rocket_id_str).first()
                        result = session.execute(rocket).scalar()

                        if result:
                            record['rocket_id'] = result.id  # Set the foreign key to the rocket's ID
                        else:
                            print(f"Rocket with ID {rocket_id_str} not found!")
                            record['rocket_id'] = None  # Handle cases where the rocket is missing
                
                return 'null'
            session.bulk_insert_mappings(table_class, data)
            session.commit()
            print(f"Successfully inserted {len(data)} records into {table_name}.")

        except Exception as e:
            print(f"Error during bulk insert into {table_name}: {e}")
            session.rollback()
        finally:
            session.close()