from orator.migrations import Migration


class CreateFavoritesTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('favorites') as table:
            table.increments('id')

            table.integer('user_id').unsigned()
            table.foreign('user_id').references('id').on('users').on_delete('cascade')

            table.integer('article_id').unsigned()
            table.foreign('article_id').references('id').on('articles').on_delete('cascade')
            
            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('favorites')
