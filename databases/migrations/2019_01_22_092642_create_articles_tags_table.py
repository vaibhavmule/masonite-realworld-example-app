from orator.migrations import Migration


class CreateArticlesTagsTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('articles_tags') as table:
            table.increments('id')

            table.integer('article_id').unsigned()
            table.foreign('article_id').references('id').on('articles')

            table.integer('tag_id').unsigned()
            table.foreign('tag_id').references('id').on('tags')
        
            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('articles_tags')
