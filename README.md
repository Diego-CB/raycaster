# 🎱 RT1: Esferas

## 📡 Tecnologias Utilizadas
- Python 🐍: Modern syntax, Interpreted Languaje
  > Python 10.0 or higher needed

# ✅Rubrica

- Criterio subjetivo. Por qué tan compleja sea su escena
- Criterio subjetivo. por qué tan visualmente atractiva sea su escena

- [x] por cada material diferente que implementen, para un máximo de 5
  - [ ] extra por cada uno de estos materiales que tenga texturas
- [x] por implementar refracción en al menos uno de sus materiales
- [x] por implementar reflexión en al menos uno de sus materiales
- [ ] por implementar figuras geométricas distintas a esferas, cubos, rectangulos y planos

## 🗃️ Estructura de Archivos

- **`src`**
  - Dentro de esta carpeta se encuentran las implementaciones de las funcionalidades de raytracing.

  - **`models`**: 
    - En esta carpeta estan las figuras geometricas a utilizar.
    - `Cube.py`: Implementacin de Cubo (ray_intersect)
    - `Plane.py`: Implementacin de Plano (ray_intersect)
    - `Sphere.py`: Implementacin de Esfera (ray_intersect)

  - **`util`**:
    - En esta carpeta se encuentran las funcionalidades generales que se utilizan en el resto del programa.
    - `bmp.py`: Escritura de archivos bmp
    - `libs.py`: Calculo de reflexion y refraccion
    - `utils.py`: Enpaquetado de colores en bytes.
    - `Vector.py`: Implementacion de Vectores 3D

- `main.py`: Contiene la definicion de Materiales a utilizar

## 🕹️ Getting Started

1. Ejecute el archivo `main.py`.
2. Si no existen errores en ejecución, se escribirá un achivo `ray.bmp` con la imagen resultante en la carpeta **`Renders`**.
  > path de la imagen: `./Renders/ray.bmp`
  > path de imagen de muestra: `./Renders/landscape_template.bmp`

## 🤓 Autor

Diego Cordova - 20212
