from sqlalchemy import *
from migrate import *

from sqlalchemy.databases import mysql

metadata = MetaData(migrate_engine)

# Tag_Property table
tag_table = Table('tag', metadata,
    Column('id', mysql.MSBigInteger(unsigned=True), autoincrement=True, primary_key=True, nullable=False),
    Column('tag', VARCHAR(128), nullable=False, index=True),
    Column('g_no', mysql.MSInteger(unsigned=True), nullable=True),
    Column('pos', VARCHAR(128), nullable=True)
)                                                                                                                    

# Tag_Association table
tag_assoc_table = Table('tag_assoc', metadata,
    Column('id', mysql.MSBigInteger(unsigned=True), autoincrement=True, primary_key=True, nullable=False),
    Column('tag_one_id', mysql.MSBigInteger(unsigned=True), nullable=False, index=True),
    Column('tag_two_id', mysql.MSBigInteger(unsigned=True), nullable=False, index=True),
    Column('score', mysql.MSInteger(unsigned=False), nullable=False), 
    Column('s_no', mysql.MSBigInteger(unsigned=False), nullable=False)
)

def upgrade():
    tag_table.create()
    tag_assoc_table.create()

def downgrade():
    tag_table.drop()
    tag_assoc_table.drop()
