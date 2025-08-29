# catalog/management/commands/create_product_groups.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from catalog.models import Product


class Command(BaseCommand):
    help = 'Создает группу модераторов продуктов и назначает разрешения'

    def handle(self, *args, **options):
        # Создаем группу модераторов
        moderator_group, created = Group.objects.get_or_create(
            name='Модератор продуктов'
        )

        if created:
            self.stdout.write('Группа "Модератор продуктов" создана')
        else:
            self.stdout.write('Группа "Модератор продуктов" уже существует')

        # Получаем разрешения
        content_type = ContentType.objects.get_for_model(Product)

        # Разрешение на отмену публикации
        unpublish_permission, created = Permission.objects.get_or_create(
            codename='can_unpublish_product',
            content_type=content_type,
            defaults={'name': 'Может отменять публикацию продукта'}
        )

        # Разрешение на удаление любого продукта
        delete_permission, created = Permission.objects.get_or_create(
            codename='can_delete_any_product',
            content_type=content_type,
            defaults={'name': 'Может удалять любой продукт'}
        )

        # Стандартные разрешения Django
        change_permission = Permission.objects.get(
            codename='change_product',
            content_type=content_type
        )
        delete_permission_std = Permission.objects.get(
            codename='delete_product',
            content_type=content_type
        )

        # Назначаем разрешения группе
        moderator_group.permissions.add(
            unpublish_permission,
            delete_permission,
            change_permission,
            delete_permission_std
        )

        self.stdout.write(
            self.style.SUCCESS('Разрешения успешно назначены группе модераторов!')
        )