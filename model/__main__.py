import click
from model.db_model import Session, engine, Base, FileType, File, User


@click.group(chain=True)
@click.pass_context
def cli(ctx):
    if ctx.invoked_subcommand is None:
        click.echo('please use a command!')


@cli.command()
def init_db():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


@cli.command()
def init_filetype():
    FileType.insert_all_types()


@cli.command()
@click.argument('name', nargs=1)
@click.argument('passwd', nargs=1)
def add_user(name, passwd):
    session = Session()
    session.add(User(username=name, password=passwd))
    session.commit()


if __name__ == "__main__":
    cli()  # pylint: disable=no-value-for-parameter
