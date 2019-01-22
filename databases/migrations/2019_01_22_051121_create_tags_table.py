from orator.migrations import Migration


class CreateTagsTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('tags') as table:
            table.increments('id')
            table.string('name').unique()
            table.timestamps()
 
    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('tags')
