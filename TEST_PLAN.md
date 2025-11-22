# 🧪 Plan de Pruebas - Dashboard Pixel

## Estado Actual
- ✅ Servidor backend corriendo en `ws://localhost:8766`
- ✅ Dashboard abierto en el navegador
- ✅ Herramienta de comparación funcionando

## 📋 Pruebas a Realizar

### Test 1: Verificar Carga de CSV
**Objetivo**: Confirmar que el CSV se carga correctamente

1. Click en botón **"📁 CSV FILE"** (debe estar activo)
2. Click en **"CLICK TO LOAD FILE"**
3. Seleccionar: `/Users/e.baena/Desktop/eeg_stream.csv`
4. **Verificar**: Nombre del archivo aparece debajo

**✅ Éxito**: Muestra "eeg_stream.csv"
**❌ Fallo**: No muestra nada o error

---

### Test 2: Verificar Preset DYNAMIC
**Objetivo**: Confirmar que el preset cambia los valores

1. Seleccionar preset **"DYNAMIC (MAX VARIETY)"**
2. **Verificar valores**:
   - Smoothing: debe mostrar **5**
   - Tempo Stability: debe mostrar **0.50**
   - Duration: debe mostrar **3.0 SEC**

**✅ Éxito**: Todos los valores cambian
**❌ Fallo**: Valores no cambian

---

### Test 3: Verificar Reproducción
**Objetivo**: Confirmar que la música suena

1. Con CSV cargado y preset DYNAMIC
2. Click **"▶ START"**
3. **Verificar**:
   - Botón START se pone verde
   - Status dice "PLAYING"
   - Active Source dice "CSV FILE"
   - Oscilloscope muestra ondas
   - Métricas se actualizan (TEMPO, SCALE, etc.)
   - **Audio suena**

**✅ Éxito**: Todo funciona, audio suena
**❌ Fallo**: No suena o no actualiza

---

### Test 4: Verificar Cambio de Escala
**Objetivo**: Confirmar que cambiar escala afecta la música

1. Con música reproduciéndose
2. Cambiar **BASE SCALE** a **"MAJOR"**
3. Esperar 10-15 segundos
4. **Verificar**: 
   - Métrica "SCALE" muestra "MAJOR"
   - Música suena más alegre/brillante

5. Cambiar a **"MINOR"**
6. Esperar 10-15 segundos
7. **Verificar**:
   - Métrica "SCALE" muestra "MINOR"
   - Música suena más melancólica/oscura

**✅ Éxito**: Escala cambia y se escucha diferente
**❌ Fallo**: Escala no cambia o suena igual

---

### Test 5: Comparar Dos CSVs
**Objetivo**: Verificar que CSVs diferentes suenan diferente

#### Parte A: CSV 1
1. STOP si está reproduciendo
2. Cargar: `/Users/e.baena/Desktop/eeg_stream.csv`
3. Preset: **DYNAMIC**
4. Base Scale: **AUTO**
5. Click **START**
6. **Escuchar durante 30 segundos**
7. **Anotar**:
   - Tempo promedio: _____
   - Escala dominante: _____
   - ¿Suena rápido o lento?: _____
   - ¿Suena alegre o triste?: _____
8. Click **STOP**

#### Parte B: CSV 2
1. Cargar: `/Users/e.baena/CascadeProjects/mindfulmakers/neurable-eeg-stream/eeg_data_20251122_143416.csv`
2. Preset: **DYNAMIC** (mismo)
3. Base Scale: **AUTO** (mismo)
4. Click **START**
5. **Escuchar durante 30 segundos**
6. **Anotar**:
   - Tempo promedio: _____
   - Escala dominante: _____
   - ¿Suena rápido o lento?: _____
   - ¿Suena alegre o triste?: _____

#### Comparación
**Según herramienta de análisis:**
- CSV1: Tempo ~96 BPM, Arousal 0.347, Energy 0.407
- CSV2: Tempo ~88 BPM, Arousal 0.232, Energy 0.297

**Diferencias esperadas:**
- ✅ CSV1 debe sonar **más rápido** (~8 BPM más)
- ✅ CSV1 debe sonar **más energético**
- ✅ CSV1 debe sonar **más fuerte**

**✅ Éxito**: Se escuchan diferencias claras
**⚠️ Parcial**: Se escuchan algunas diferencias
**❌ Fallo**: Suenan iguales

---

### Test 6: Verificar Preset BALANCED vs DYNAMIC
**Objetivo**: Confirmar que presets diferentes suenan diferente

#### Con BALANCED
1. Cargar cualquier CSV
2. Preset: **BALANCED**
3. START, escuchar 20 segundos
4. **Anotar**: ¿Cuántos cambios de tempo notas? _____

#### Con DYNAMIC
1. STOP
2. Preset: **DYNAMIC**
3. START, escuchar 20 segundos
4. **Anotar**: ¿Cuántos cambios de tempo notas? _____

**Diferencias esperadas:**
- BALANCED: Cambios lentos, frases largas (6s)
- DYNAMIC: Cambios rápidos, frases cortas (3s)

**✅ Éxito**: DYNAMIC suena más variado
**❌ Fallo**: Suenan igual

---

## 📊 Resultados Esperados

### Herramienta de Comparación
```bash
python compare_csvs.py csv1.csv csv2.csv 50
```

**Debe mostrar:**
- Diferencias en tempo, arousal, energy
- Recomendaciones
- Assessment de si suenan diferentes

### Dashboard
**Debe funcionar:**
- ✅ Carga de CSV
- ✅ Cambio de presets
- ✅ Cambio de escala base
- ✅ Reproducción de audio
- ✅ Visualización en oscilloscope
- ✅ Actualización de métricas
- ✅ Start/Stop

**Debe sonar diferente:**
- ✅ Entre CSVs diferentes
- ✅ Entre escalas diferentes (MAJOR vs MINOR)
- ✅ Entre presets diferentes (BALANCED vs DYNAMIC)

---

## 🐛 Problemas Conocidos

### ❌ Si no suena nada:
1. Verificar que sounddevice está instalado
2. Verificar que hay dispositivo de audio
3. Revisar logs del servidor backend

### ❌ Si no cambia la escala:
1. Verificar en consola del navegador (F12)
2. Debe mostrar: `🎼 Base scale set to: major`
3. Verificar logs del backend

### ❌ Si suenan iguales dos CSVs:
1. Verificar con herramienta de comparación primero
2. Si herramienta muestra diferencias pero no se escuchan:
   - Usar preset DYNAMIC
   - Reducir smoothing a 5
   - Reducir duration a 3s

---

## ✅ Checklist Final

Antes de hacer commit, verificar:

- [ ] CSV se carga correctamente
- [ ] Presets cambian los valores
- [ ] Audio reproduce
- [ ] Oscilloscope actualiza
- [ ] Métricas actualizan
- [ ] Cambio de escala funciona
- [ ] CSVs diferentes suenan diferentes
- [ ] Presets diferentes suenan diferentes
- [ ] Start/Stop funcionan
- [ ] No hay errores en consola

---

**Fecha de prueba**: ___________
**Probado por**: ___________
**Resultado**: ⬜ PASS  ⬜ FAIL  ⬜ PARCIAL
