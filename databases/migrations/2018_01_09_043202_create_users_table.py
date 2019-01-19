from orator.migrations import Migration


class CreateUsersTable(Migration):

    def up(self):
        """Run the migrations."""
        with self.schema.create('users') as table:
            table.increments('id')
            table.string('username')
            table.string('email').unique()
            table.string('password')
            table.text('token').nullable()
            table.string('remember_token').nullable()
            table.string('bio').nullable()
            table.string('image').nullable()
            table.timestamps()

    def down(self):
        """Revert the migrations."""
        self.schema.drop('users')
