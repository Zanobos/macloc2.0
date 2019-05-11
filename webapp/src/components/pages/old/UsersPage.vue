<template>
  <b-container>
    <b-row class="mt-2">
      <b-col>
        <insert-user></insert-user>
      </b-col>
      <b-col>
        <list-users></list-users>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
import ListUsers from '@/components/collections/ListUsers.vue'
import InsertUser from '@/components/subpages/InsertUser.vue'

export default {
  name: 'UsersPage',
  components: {
    ListUsers,
    InsertUser
  }
}
</script>
