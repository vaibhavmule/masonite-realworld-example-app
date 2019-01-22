from orator.migrations import Migration


class CreateCommentsTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('comments') as table:
            table.increments('id')
            table.text('body')

            table.integer('article_id').unassined()
            table.foreign('article_id').references('id').on('articles')

            table.integer('author_id').unassined()
            table.foreign('author_id').references('id').on('users')
            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('comments')
