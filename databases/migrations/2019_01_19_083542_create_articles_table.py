from orator.migrations import Migration


class CreateArticlesTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('articles') as table:
            table.increments('id')

            table.string('slug').unique()
            table.string('title')
            table.string('description')
            table.text('body')

            table.integer('author_id').unsigned()
            table.foreign('author_id').references('id').on('users')

            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('articles')
