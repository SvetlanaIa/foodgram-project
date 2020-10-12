from django.db import models
from django.contrib.auth import get_user_model



User = get_user_model()



class Tag (models.Model):
    name=models.TextField(verbose_name='Название тега')
    slug = models.SlugField(
        verbose_name='Тэг',
        unique=True,max_length=100,
    )
    style=models.CharField(max_length=100,blank=True,null=True)

    def __str__(self):
        return self.slug



class Ingredient (models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    dimension = models.CharField(
        max_length=100,blank=True,null=True, verbose_name='Единицы измерения')

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'   
        ordering = ('name', )

    def __str__(self):
        return self.name     



class Recipe (models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="recipes",verbose_name='Автор публикации',)
    name = models.CharField(
        verbose_name='Название рецепта',
        max_length=200
    )
    image = models.ImageField(
      #  upload_to=nameFile)
      upload_to="recipes/",)

    description = models.CharField(max_length=280)
    ingredients = models.ManyToManyField(
        Ingredient,related_name= 'recipes',
         through='Ingredient_Recipe',
         through_fields=('recipe','ingredient'),
    )
      
   
   

    tag = models.ManyToManyField(
        Tag, related_name='recipes', verbose_name='Теги'
        # through='Tag_Recipe',
        # through_fields=('recipe','tag')
    )
    time = models.PositiveIntegerField(verbose_name='Время приготовления в минутах')
    slug = models.SlugField(
        verbose_name='URL slug',
        unique=True,
        blank=True,null=True
    )
    pub_date=models.DateField(
        verbose_name='Дата публикации', auto_now_add=True)

    def __str__(self):
        return self.name   

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-pub_date', )



# class Tag_Recipe(models.Model):
#     recipe = models.ForeignKey(
#         Recipe,
#         on_delete=models.CASCADE
#     )
#     tag = models.ForeignKey(
#         Tag,
#         on_delete=models.CASCADE
#     )

class Ingredient_Recipe(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,blank=True,null=True)
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,blank=True,null=True)
    amount = models.FloatField(verbose_name='Количество',default=0,blank=True,null=True)
    def __str__(self):
        return f'{self.ingredient} для {self.recipe}'

    

class Follow(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="follower")
    author = models.ManyToManyField(
        User, related_name='following', verbose_name='Избранный автор',
        blank=True)

    def __str__(self):
        return f'Подписки {self.user}'

    class Meta:
        verbose_name = "Подписка на автора"
        verbose_name_plural = "Подписки на авторов"       
    
class Favorite(models.Model):
    recipes = models.ManyToManyField(
        Recipe, related_name='favorite_recipes', verbose_name='Рецепты',
        blank=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_for_favorite")   
    

    def __str__(self):
        return f'Избранные рецепты {self.user}'

    class Meta:
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'    
      
class ShopList(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='shop_list',
        verbose_name='Пользователь')

    recipes = models.ManyToManyField(
        Recipe, related_name='shop_list', verbose_name='Рецепты', blank=True)

    def __str__(self):
        return f'Список покупок {self.user}'

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'      