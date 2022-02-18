<template>
  <img
    v-if="valid"
    :alt="user.name"
    :class="{'w-8 h-8': size === 'mini', 'w-16 h-16': size === 'small', 'w-24 h-24': size === 'medium'}"
    :src="user.avatar"
    class="rounded-full"
  >
</template>

<script lang="ts">
import Vue from 'vue'
import { User } from '~/kb_client/models/User'

export default Vue.extend({
  name: 'UserAvatar',
  props: {
    user: {
      type: Object as () => User,
      required: true
    },
    size: {
      type: String,
      default: 'small'
    }
  },
  data () {
    return {
      valid: false
    }
  },
  watch: {
    user: {
      immediate: true,
      deep: true,
      async handler (val) {
        try {
          const res = await this.$axios.get(val.avatar)
          this.valid = res.status === 200

          return
        } catch (err) {
          this.valid = err.message.includes('Network Error')

          return
        }

        this.valid = false
      }
    }
  }
})
</script>
