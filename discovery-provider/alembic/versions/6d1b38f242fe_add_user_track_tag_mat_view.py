"""add user track tag mat view

Revision ID: 6d1b38f242fe
Revises: 47b07608863f
Create Date: 2020-11-23 15:57:28.424094

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6d1b38f242fe'
down_revision = '47b07608863f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    connection = op.get_bind()
    connection.execute('''
    --- Create matviews for easier user and track tag search querying
    CREATE MATERIALIZED VIEW tag_track_user AS
	SELECT
        UNNEST(tags) AS tag,
        track_id,
        owner_id
    FROM
    (
        SELECT
            string_to_array(LOWER(tracks.tags), ',') AS tags,
            track_id,
            owner_id
        FROM
            tracks
        WHERE
            tags <> ''
            AND tags IS NOT NULL 
            AND is_current IS TRUE
            AND is_unlisted IS FALSE
            AND stem_of IS NULL
        ORDER BY
            updated_at DESC
    ) AS t
    GROUP BY
        tag,
        track_id,
        owner_id;
    
    CREATE INDEX tag_track_user_tag_idx ON tag_track_user (tag);
    CREATE UNIQUE INDEX tag_track_user_idx ON tag_track_user (tag, track_id, owner_id);
    ''')

def downgrade():
    connection = op.get_bind()
    connection.execute('''
    DROP INDEX IF EXISTS tag_track_user_tag_idx;
    DROP INDEX IF EXISTS tag_track_user_idx;
    DROP MATERIALIZED VIEW tag_track_user;
    ''')