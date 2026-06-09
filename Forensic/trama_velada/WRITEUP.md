# Writeup: Trama Velada

## Análisis

La captura `traffic.pcap` contiene una sesión HTTPS sobre TLS 1.3. Sin el archivo `keylog.txt` el contenido queda cifrado, así que el primer paso es descifrar la sesión con `tshark` o Wireshark.

## Resolución

1. **Descifrar TLS**
   - Cargá `keylog.txt` con `-o tls.keylog_file:keylog.txt`.
   - Filtrá por `http.response` para ver las respuestas reconstruidas.

2. **Extraer el seed**
   - La primera respuesta viene con `Content-Encoding: gzip`.
   - `tshark` reconstruye el objeto HTTP y expone el cuerpo como `http.file_data`.
   - Ese JSON contiene el campo:
     - `seed = "rosebud"`

3. **Extraer el payload final**
   - La segunda respuesta usa `Transfer-Encoding: chunked`.
   - Su cuerpo es una cadena base64 ofuscada con XOR usando el seed anterior.

4. **Decodificar**
   - Base64 -> bytes cifrados.
   - XOR con `rosebud` repetido.
   - Resultado final:
     - `H4L{tls_gzip_xor_chain_2026}`

## Comando útil

```bash
tshark -r traffic.pcap -o tls.keylog_file:keylog.txt -Y http.response -T fields -e frame.number -e http.content_encoding -e http.transfer_encoding -e http.file_data
```

## Flag

`H4L{tls_gzip_xor_chain_2026}`
