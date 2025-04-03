from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UsuarioManager(BaseUserManager):
    def create_user(self, email, nome_completo, password=None):
        if not email:
            raise ValueError('email inválido')
        
        usuario = self.model (
            email = self.normalize_email(email),
            nome_completo = nome_completo,
        )
        
        usuario.set_password(password)
        usuario.save(using = self._db)
        return usuario

    def create_superuser(self, email, nome_completo, password=None):
        usuario = self.create_user(
            email=email,
            nome_completo=nome_completo,
            password=password
        )
        usuario.is_admin = True
        usuario.save(using=self._db)
        return usuario

class Usuario(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email',
        max_length=255,
        unique=True
    )
    
    nome_completo = models.CharField(max_length=255)
    data_criacao = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome_completo']
    
    objects = UsuarioManager()
    
    def __str__(self):
        return self.nome_completo
    
    def has_perm(self, perm, obj=None):
        return True
    
    def has_module_perms(self, app_label):
        return True
    
    @property
    def is_staff(self):
        return self.is_admin

class Medico(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, primary_key=True)
    crm = models.CharField(max_length=15, unique=True)
    
    def __str__(self):
        return f"{self.usuario.nome_completo} (CRM: {self.crm})"

class Enfermeiro(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, primary_key= True)
    coren = models.CharField(max_length=15, unique=True)
    
    def __str__(self):
        return f"{self.usuario.nome_completo} (COREN: {self.coren})"

class Farmaceutico(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, primary_key=True)
    crf = models.CharField(max_length=15, unique=True)
    
    def __str__(self):
        return f"{self.usuario.nome_completo} (CRF: {self.crf})"

class Paciente(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, primary_key=True)
    cpf = models.CharField(max_length=14, unique=True)
    data_nascimento = models.DateField()
    
    def __str__(self):
        return f"Paciente: {self.usuario.nome_completo}"