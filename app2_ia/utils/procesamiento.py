def preparar_datos_para_limpiar(lista_de_registros):
    return [{"texto": registro["valoracion_gpt"]} for registro in lista_de_registros]
