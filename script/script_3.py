import numpy as np
import time

class MarcoAlgebraicoVectorizado:
    """
    Implementacion del marco algebraico vectorizado.
    Resuelve y evoluciona campos tensoriales eliminando friccion computacional.
    No modifica la fisica: solo reorganiza la ejecucion para aprovechar la arquitectura del procesador.
    """

    @staticmethod
    def esquema_tradicional(dominio, funcion_metrica):
        """
        Enfoque convencional: bucle punto por punto.
        Representa como se resuelven habitualmente las metricas en la mayoria de codigos.
        """
        t0 = time.perf_counter()
        resultado = np.zeros_like(dominio, dtype=np.float64)
        for i in range(len(dominio)):
            resultado[i] = funcion_metrica(dominio[i])
        tiempo_total = time.perf_counter() - t0
        return resultado, tiempo_total

    @staticmethod
    def esquema_vectorizado(dominio, funcion_metrica):
        """
        Enfoque optimizado: operaciones sobre todo el dominio en un solo flujo continuo.
        Equivalente matematico, pero estructurado para ejecucion paralela nativa.
        """
        t0 = time.perf_counter()
        resultado = funcion_metrica(dominio)
        tiempo_total = time.perf_counter() - t0
        return resultado, tiempo_total

    @staticmethod
    def funcion_metrica_warp(x):
        """
        Perfil de curvatura tipo métrica de curvatura.
        f(r) = (tanh(sigma(r + R)) - tanh(sigma(r - R))) / (2 tanh(sigma R))
        Funcion de forma que define la region de deformacion del espaciotiempo.
        """
        sigma = 2.0
        R = 1.0
        return (np.tanh(sigma * (x + R)) - np.tanh(sigma * (x - R))) / (2.0 * np.tanh(sigma * R))

    @staticmethod
    def funcion_campo_coherencia(x):
        """
        Perfil de campo de coherencia TCDS: R ∝ ∇²Σ.
        Segunda derivada de un perfil gaussiano de coherencia.
        """
        sigma = 0.3
        return (1.0 - (x / sigma)**2) * np.exp(-x**2 / (2.0 * sigma**2))

    @staticmethod
    def ejecutar_comparacion(puntos=2000000):
        print("=" * 70)
        print("MARCO ALGEBRAICO VECTORIZADO - COMPARACION DE RENDIMIENTO")
        print("=" * 70)
        print(f"Puntos de malla: {puntos:,}")
        print()

        dominio = np.linspace(-3.0, 3.0, puntos)

        print("--- PERFIL METRICA DE CURVATURA ---")
        res_trad, t_trad = MarcoAlgebraicoVectorizado.esquema_tradicional(
            dominio, MarcoAlgebraicoVectorizado.funcion_metrica_warp)
        res_vec, t_vec = MarcoAlgebraicoVectorizado.esquema_vectorizado(
            dominio, MarcoAlgebraicoVectorizado.funcion_metrica_warp)

        aceleracion = t_trad / t_vec
        coinciden = np.allclose(res_trad, res_vec)

        print(f"Tradicional:    {t_trad * 1000:>10.2f} ms")
        print(f"Vectorizado:    {t_vec * 1000:>10.2f} ms")
        print(f"Aceleracion:    {aceleracion:>10.1f} veces")
        print(f"Exactitud:      {'IDENTICA' if coinciden else 'DIFERENTE'}")
        print()

        print("--- CAMPO DE COHERENCIA TCDS (R ∝ ∇²Σ) ---")
        res_trad, t_trad = MarcoAlgebraicoVectorizado.esquema_tradicional(
            dominio, MarcoAlgebraicoVectorizado.funcion_campo_coherencia)
        res_vec, t_vec = MarcoAlgebraicoVectorizado.esquema_vectorizado(
            dominio, MarcoAlgebraicoVectorizado.funcion_campo_coherencia)

        aceleracion = t_trad / t_vec
        coinciden = np.allclose(res_trad, res_vec)

        print(f"Tradicional:    {t_trad * 1000:>10.2f} ms")
        print(f"Vectorizado:    {t_vec * 1000:>10.2f} ms")
        print(f"Aceleracion:    {aceleracion:>10.1f}veces")
        print(f"Exactitud:      {'IDENTICA' if coinciden else 'DIFERENTE'}")
        print()

        print("=" * 70)
        print("CONCLUSION")
        print("=" * 70)
        print("El marco vectorizado no modifica la fisica: el resultado es identico.")
        print("Lo que cambia es la estructura de ejecucion: de bucle secuencial")
        print("a flujo continuo sobre todo el dominio, eliminando friccion computacional.")
        print("Esto permite explorar mayor resolucion, mallas mas finas y evoluciones")
        print("mas largas sin incrementar los recursos de hardware.")
        print("=" * 70)

        return {
            "puntos": puntos,
            "aceleracion_metrica": t_trad / t_vec,
            "exactitud_identica": coinciden
        }

if __name__ == "__main__":
    MarcoAlgebraicoVectorizado.ejecutar_comparacion()
