from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import StudentProductAccess, Group

@receiver(post_save, sender=StudentProductAccess)
@receiver(post_delete, sender=StudentProductAccess)
def create_group_for_product(sender, instance, **kwargs):
    if instance.has_access:
        product = instance.product
        student_product_access_count = StudentProductAccess.objects.filter(product=product).count() # Количество учеников
        student_product_access_list = StudentProductAccess.objects.filter(product=product) # Список учеников

        # АЛГОРИТМ РАСПРЕДЕЛЕНИЯ В ГРУППЫ
        groups = Group.objects.filter(product=product)
        groups.delete() # Удаляем все существующие группы

        num_groups = student_product_access_count // product.max_group_size  # Определяем количество групп
        remains = student_product_access_count % product.max_group_size  # Определяем остаток учеников

        if remains > 0:
            num_groups += 1

        # Формируем список из ID всех студентов
        student_course = []  # Создаем переменную с ID всех учеников данного продукта
        for access in student_product_access_list:
            user_unique_id = access.student.id
            student_course.append(user_unique_id)


        for i in range(num_groups): # Перебираем все группы
            group_name = f"{product.name}_group_{i + 1}"
            group = Group.objects.create(product=product, title=group_name)  # Создаем новую группу

            for j in range(student_product_access_count // num_groups):
                # Добавляем до максимального количество студентов в группу
                student_id_to_add = student_course[0]  # Выбираем первого студента из группы
                student_to_add = StudentProductAccess.objects.filter(student_id=student_id_to_add).first()
                group.users.add(student_to_add.student)  # Добавляем первого студента из группы
                student_course.remove(student_id_to_add)  # Удаляем первого студента из группы


        if len(student_course) != 0: # Проверяем остались ли не распределенные студенты
            all_groups = Group.objects.filter(product=product)

            for i in range(len(student_course)):
                group = all_groups[i]
                student_id_to_add = student_course[0]  # Выбираем первого студента из группы
                student_to_add = StudentProductAccess.objects.filter(student_id=student_id_to_add).first()
                group.users.add(student_to_add.student)  # Добавляем первого студента из группы
                student_course.remove(student_id_to_add)









