<template>
  <div class="home">
    <el-row :gutter="40">
      <!-- Левая панель - Загрузка файла -->
      <el-col :xs="24" :md="12">
        <el-card class="upload-card">
          <template #header>
            <div class="card-header">
              <el-icon><Upload /></el-icon>
              <span>Загрузка документа</span>
            </div>
          </template>
          
          <el-upload
            ref="uploadRef"
            :auto-upload="false"
            :show-file-list="true"
            :limit="1"
            :on-change="handleFileChange"
            :on-remove="handleFileRemove"
            :file-list="fileList"
            drag
            accept=".docx,.pdf,.txt,.rtf"
          >
            <el-icon class="el-icon--upload"><upload-filled /></el-icon>
            <div class="el-upload__text">
              Перетащите файл сюда или <em>нажмите для загрузки</em>
            </div>
            <template #tip>
              <div class="el-upload__tip">
                Поддерживаемые форматы: {{ supportedFormats.join(', ') }}
              </div>
            </template>
          </el-upload>
          
          <!-- Настройки конвертации -->
          <div class="conversion-options" v-if="selectedFile">
            <h3>Настройки конвертации</h3>
            
            <el-form :model="conversionOptions" label-width="200px">
              <el-form-item label="Сохранять форматирование">
                <el-switch v-model="conversionOptions.preserve_formatting" />
              </el-form-item>
              
              <el-form-item label="Включать изображения">
                <el-switch v-model="conversionOptions.include_images" />
              </el-form-item>
              
              <el-form-item label="Максимальный размер изображения">
                <el-input-number 
                  v-model="conversionOptions.max_image_size" 
                  :min="100" 
                  :max="2048"
                  :step="100"
                />
              </el-form-item>
              
              <el-form-item label="Формат таблиц">
                <el-select v-model="conversionOptions.table_format">
                  <el-option label="Grid" value="grid" />
                  <el-option label="Simple" value="simple" />
                  <el-option label="Pipe" value="pipe" />
                </el-select>
              </el-form-item>
            </el-form>
            
            <el-button 
              type="primary" 
              size="large" 
              :loading="isLoading"
              :disabled="!selectedFile"
              @click="convertDocument"
              class="convert-button"
            >
              <el-icon><Document /></el-icon>
              Конвертировать
            </el-button>
          </div>
        </el-card>
      </el-col>
      
      <!-- Правая панель - Результат -->
      <el-col :xs="24" :md="12">
        <el-card class="result-card">
          <template #header>
            <div class="card-header">
              <el-icon><Document /></el-icon>
              <span>Результат конвертации</span>
            </div>
          </template>
          
          <div v-if="error" class="error-message">
            <el-alert
              :title="error"
              type="error"
              :closable="false"
              show-icon
            />
          </div>
          
          <div v-else-if="conversionResult && conversionResult.success" class="conversion-result">
            <div class="result-header">
              <h3>Конвертация завершена успешно!</h3>
              <el-button 
                type="success" 
                size="small"
                @click="downloadMarkdown"
              >
                <el-icon><Download /></el-icon>
                Скачать Markdown
              </el-button>
            </div>
            
            <div class="preview-tabs">
              <el-tabs v-model="activeTab">
                <el-tab-pane label="Предварительный просмотр" name="preview">
                  <div class="markdown-preview" v-html="renderedMarkdown"></div>
                </el-tab-pane>
                <el-tab-pane label="Исходный код" name="source">
                  <el-input
                    v-model="conversionResult.content"
                    type="textarea"
                    :rows="20"
                    readonly
                  />
                </el-tab-pane>
              </el-tabs>
            </div>
          </div>
          
          <div v-else class="empty-state">
            <el-empty description="Загрузите документ для конвертации" />
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useStore } from 'vuex'
import { marked } from 'marked'
import { ElMessage } from 'element-plus'

export default {
  name: 'Home',
  setup() {
    const store = useStore()
    const uploadRef = ref(null)
    const fileList = ref([])
    const selectedFile = ref(null)
    const activeTab = ref('preview')
    
    const conversionOptions = ref({
      preserve_formatting: true,
      include_images: true,
      max_image_size: 1024,
      table_format: 'grid'
    })
    
    // Computed properties
    const supportedFormats = computed(() => store.state.supportedFormats)
    const isLoading = computed(() => store.state.isLoading)
    const error = computed(() => store.state.error)
    const conversionResult = computed(() => store.state.conversionResult)
    
    const renderedMarkdown = computed(() => {
      if (conversionResult.value?.content) {
        return marked(conversionResult.value.content)
      }
      return ''
    })
    
    // Methods
    const handleFileChange = (file) => {
      selectedFile.value = file.raw
      fileList.value = [file]
    }
    
    const handleFileRemove = () => {
      selectedFile.value = null
      fileList.value = []
    }
    
    const convertDocument = async () => {
      if (!selectedFile.value) {
        ElMessage.warning('Пожалуйста, выберите файл для конвертации')
        return
      }
      
      await store.dispatch('convertDocument', {
        file: selectedFile.value,
        options: conversionOptions.value
      })
    }
    
    const downloadMarkdown = () => {
      if (!conversionResult.value?.content) return
      
      const blob = new Blob([conversionResult.value.content], { type: 'text/markdown' })
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = conversionResult.value.filename || 'converted.md'
      document.body.appendChild(a)
      a.click()
      document.body.removeChild(a)
      URL.revokeObjectURL(url)
      
      ElMessage.success('Файл успешно скачан')
    }
    
    // Lifecycle
    onMounted(async () => {
      await store.dispatch('fetchSupportedFormats')
    })
    
    return {
      uploadRef,
      fileList,
      selectedFile,
      activeTab,
      conversionOptions,
      supportedFormats,
      isLoading,
      error,
      conversionResult,
      renderedMarkdown,
      handleFileChange,
      handleFileRemove,
      convertDocument,
      downloadMarkdown
    }
  }
}
</script>

<style scoped>
.home {
  padding: 20px 0;
}

.upload-card,
.result-card {
  height: 100%;
  min-height: 600px;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 18px;
  font-weight: 600;
}

.conversion-options {
  margin-top: 30px;
  padding-top: 20px;
  border-top: 1px solid #ebeef5;
}

.conversion-options h3 {
  margin-bottom: 20px;
  color: #303133;
}

.convert-button {
  margin-top: 20px;
  width: 100%;
}

.error-message {
  margin-bottom: 20px;
}

.conversion-result {
  height: 100%;
}

.result-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.result-header h3 {
  margin: 0;
  color: #67c23a;
}

.preview-tabs {
  height: calc(100% - 80px);
}

.markdown-preview {
  padding: 20px;
  background: #fafafa;
  border-radius: 4px;
  max-height: 500px;
  overflow-y: auto;
  line-height: 1.6;
}

.markdown-preview :deep(h1),
.markdown-preview :deep(h2),
.markdown-preview :deep(h3) {
  color: #303133;
  margin-top: 20px;
  margin-bottom: 10px;
}

.markdown-preview :deep(p) {
  margin-bottom: 10px;
}

.markdown-preview :deep(code) {
  background: #f0f0f0;
  padding: 2px 4px;
  border-radius: 3px;
  font-family: 'Courier New', monospace;
}

.markdown-preview :deep(pre) {
  background: #f5f5f5;
  padding: 15px;
  border-radius: 4px;
  overflow-x: auto;
}

.empty-state {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 400px;
}

/* Responsive design */
@media (max-width: 768px) {
  .home {
    padding: 10px 0;
  }
  
  .result-header {
    flex-direction: column;
    gap: 10px;
    align-items: flex-start;
  }
}
</style>
