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
            table.foreign('article_id').references('id').on('articles').on_delete('cascade')

            table.integer('author_id').unassined()
            table.foreign('author_id').references('id').on('users').on_delete('cascade')
            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('comments')
