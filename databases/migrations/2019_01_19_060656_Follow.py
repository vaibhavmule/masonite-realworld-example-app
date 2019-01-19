from orator.migrations import Migration


class Follow(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('follows') as table:
            table.integer('user_id').unsigned()
            table.integer('follower_id').unsigned()

            table.foreign('user_id').references('id').on('users').on_delete('cascade')
            table.foreign('follower_id').references('id').on('users').on_delete('cascade')
            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        pass
