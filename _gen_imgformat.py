import io, base64
tmpl = '<template>
<view class="page">
  <view class="custom-nav" :style="{ paddingTop: statusBarHeight + 'px' }">
    <view class="nav-row">
      <text class="nav-icon" @click="goBack">←</text>
      <text class="nav-title">图片格式转换</text>
      <text class="nav-icon"> </text>
    </view>
  </view>
  <view class="content">
    <view class="pick-btn" @click="pickImage" v-if="!tempFilePath">
      <text class="pick-btn-text">+ 选择图片</text>
    </view>
    <view v-if="tempFilePath">
      <view class="preview-box">
        <image :src="tempFilePath" mode="aspectFit" class="preview-img"></image>
      </view>
      <view class="info-row">
        <text class="info-label">原始大小：</text>
        <text class="info-value">{{ originalSize }}</text>
      </view>
      <view class="info-row">
        <text class="info-label">尺寸：</text>
        <text class="info-value">{{ imageWidth }} x {{ imageHeight }}</text>
      </view>
      <view class="section-title">选择目标格式</view>
      <view class="format-btns">
        <view class="fmt-btn" :class="{ active: targetFormat === 'jpeg' }" @click="targetFormat = 'jpeg'">JPEG</view>
        <view class="fmt-btn" :class="{ active: targetFormat === 'png' }" @click="targetFormat = 'png'">PNG</view>
        <view class="fmt-btn" :class="{ active: targetFormat === 'webp' }" @click="targetFormat = 'webp'">WEBP</view>
      </view>
      <view v-if="targetFormat === 'jpeg'" class="quality-row">
        <text class="info-label">质量：{{ quality }}%</text>
        <slider class="quality-slider" :value="quality" min="10" max="100" @change="onQualityChange" block-size="20" block-color="#06b6d4" activeColor="#06b6d4" backgroundColor="#ddd"/>
      </view>
      <view v-if="convertedSize" class="info-row">
        <text class="info-label">转换后大小：</text>
        <text class="info-value highlight">{{ convertedSize }}</text>
      </view>
      <view class="action-row">
        <view class="action-btn convert-btn" @click="convertFormat">转换</view>
        <view class="action-btn save-btn" @click="saveImage" v-if="convertedPath">保存到相册</view>
      </view>
    </view>
  </view>
  <canvas canvas-id="convertCanvas" :style="{ width: imageWidth + 'px', height: imageHeight + 'px', position: 'fixed', left: '-9999px' }"></canvas>
</view>
</template>'
