<template>
  <div id="app">
    <el-container>
      <el-header>
        <div class="header-content">
          <h1>Document Converter</h1>
          <p>Конвертация документов в markdown с помощью docling</p>
        </div>
      </el-header>
      
      <el-main>
        <router-view />
      </el-main>
      
      <el-footer>
        <div class="footer-content">
          <p>&copy; 2024 Document Converter. Powered by docling.</p>
        </div>
      </el-footer>
    </el-container>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
#app {
  font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', '微软雅黑', Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  min-height: 100vh;
}

.el-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  text-align: center;
  padding: 20px 0;
}

.header-content h1 {
  margin: 0;
  font-size: 2.5rem;
  font-weight: 300;
}

.header-content p {
  margin: 10px 0 0 0;
  font-size: 1.1rem;
  opacity: 0.9;
}

.el-main {
  padding: 40px 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.el-footer {
  background-color: #f5f5f5;
  text-align: center;
  padding: 20px 0;
  color: #666;
}

.footer-content p {
  margin: 0;
  font-size: 0.9rem;
}

/* Responsive design */
@media (max-width: 768px) {
  .header-content h1 {
    font-size: 2rem;
  }
  
  .header-content p {
    font-size: 1rem;
  }
  
  .el-main {
    padding: 20px 10px;
  }
}
</style>
