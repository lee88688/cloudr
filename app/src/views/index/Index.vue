<template>
  <a-layout style="height: 100%;">
    <a-layout-header class="header-bar">
      <div class="brand">
        <a-icon type="cloud" /><span>cloudr</span>
      </div>
    </a-layout-header>
    <a-layout>
      <a-layout-sider width="200" style="background: #fff">
        <a-menu mode="inline">
          <a-menu-item>
            <a-icon type="folder" />
            <span>全部文件</span>
          </a-menu-item>
          <a-menu-item>
            <span>图片</span>
          </a-menu-item>
          <a-menu-item>
            <span>文档</span>
          </a-menu-item>
          <a-menu-item>
            <span>视频</span>
          </a-menu-item>
        </a-menu>
      </a-layout-sider>
      <a-layout>
        <a-layout-content>
          content
        </a-layout-content>
      </a-layout>
    </a-layout>
  </a-layout>
</template>

<script>
export default {
  name: 'Index'
}
</script>

<style lang="scss" scoped>
.header-bar {
  color: #fff;
  display: flex;
  justify-content: start;
  align-content: center;

  .brand {
    font-size: 20px;
    cursor: pointer;

    > span {
      margin-left: 10px;
    }
  }
}
</style>
