<template>
<v-container class="pa-2 edit-form" >
  <div v-if="this.currentItem">
    <h1>Item details</h1>

    <v-form ref="form" lazy-validation>
      <v-text-field
        v-model="currentItem.id"
        label="ID"
        readonly
        shaped
        filled
      ></v-text-field>

      <v-text-field
        v-model="currentItem.name"
        :rules="[(v) => !!v || 'Name is required']"
        label="Name"
        required
        outlined
      ></v-text-field>

      <v-radio-group label="Type" v-model="currentItem.type">
        <v-radio name="type" label="Tool" value="tool"></v-radio>
        <v-radio name="type" label="Command" value="command"></v-radio>                
      </v-radio-group>

      <v-textarea
          label="Description"
          :rules="[(v) => !!v || 'Description is required']"
          required
          hint="Description, keywords"
          v-model="currentItem.description"
          outlined
        ></v-textarea>

        <v-textarea
          label="Usage"
          :rules="[(v) => !!v || 'Usage is required']"
          required
          hint="Usage, commands"
          v-model="currentItem.usage"
          outlined
        ></v-textarea>

        <v-text-field
        v-model="currentItem.source"
        label="Source/site"
        :rules="[(v) => !!v || 'Usage is required']"
        required
        outlined
      ></v-text-field>

      <v-text-field
        v-model="currentItem.cve"
        label="CVE"
        outlined
      ></v-text-field>

      <v-row>
        <v-col>
          <p>Attack OS(es)</p>
        </v-col>
      </v-row>
      <hr>
      <v-row>
          <v-col
            cols="12"
            sm="3"
            md="3"
          >
            <v-checkbox
              v-model="currentItem.attackos"
              label="linux"
              value="linux"
              hide-details
            ></v-checkbox>
            <v-checkbox
              v-model="currentItem.attackos"
              label="windows"
              value="windows"
              hide-details
            ></v-checkbox>
          </v-col>
          <v-col
            cols="12"
            sm="3"
            md="3"
          >
            <v-checkbox
              v-model="currentItem.attackos"
              label="mac"
              value="mac"
              hide-details
            ></v-checkbox>
            <v-checkbox
              v-model="currentItem.attackos"
              label="other"
              value="other"
              hide-details
            ></v-checkbox>
          </v-col>
      </v-row>

      <v-row>
        <v-col>
          <p>Phases</p>
        </v-col>
      </v-row>
      <hr>

        <v-row>
          <v-col
            cols="12"
            sm="3"
            md="3"
          >
            <v-checkbox
              v-model="currentItem.phase"
              label="recon"
              value="recon"
              hide-details
            ></v-checkbox>
            <v-checkbox
              v-model="currentItem.phase"
              label="scanning"
              value="scanning"
              hide-details
            ></v-checkbox>
          </v-col>
          <v-col
            cols="12"
            sm="3"
            md="3"
          >
            <v-checkbox
              v-model="currentItem.phase"
              label="initial foothold"
              value="initial foothold"
              hide-details
            ></v-checkbox>
            <v-checkbox
              v-model="currentItem.phase"
              label="privesc"
              value="privesc"
              hide-details
            ></v-checkbox>
          </v-col>
          <v-col
            cols="12"
            sm="3"
            md="3"
          >
            <v-checkbox
              v-model="currentItem.phase"
              label="maintain access"
              value="maintain access"
              hide-details
            ></v-checkbox>
            <v-checkbox
              v-model="currentItem.phase"
              label="covering"
              value="covering"
              hide-details
            ></v-checkbox>
          </v-col>
          <v-col
            cols="12"
            sm="3"
            md="3"
          >
            <v-checkbox
              v-model="currentItem.phase"
              label="general"
              value="general"
              hide-details
            ></v-checkbox>
          </v-col>
        </v-row>

      
        <div class="text-center mt-3 pa-3">
          <v-btn color="success"  @click="updateItem" >
            Update
          </v-btn>
        </div>
    </v-form>
  </div>

  <div v-else>
    <p>Please select an item...</p>
  </div>
</v-container>
</template>

<script>
import axios from 'axios';

export default {
  name: "tutorial",
  data: function() {
    return {
      data: null,
      currentItem: null,
    };
  },
  methods: {
    getItem(id) {
      const path = 'http://localhost:5000/api/item/'+ id;
      axios.get(path, )
        .then((res) => {
          this.data = res.data;
          this.currentItem = this.data.item
          //console.log(this.currentItem.attackos)
        })
        .catch((error) => {
          console.error(error);
        });
    },
    updateItem() {
      console.log(this.currentItem)
    },
    // checkOses(self) {
    // this.currentItem.attackos.forEach(os => {
    //     if (os == 'linux') {
    //       self.linux = true
    //     }
    //     else if (os == 'windows'){
    //       self.windows = true  
    //     }
    //     else if (os == 'mac'){
    //       self.mac = true  
    //     }
    //     else if (os == 'other'){
    //       self.other = true  
    //     }
    // });
    // }
  },
  mounted() {
    this.getItem(this.$route.params.id);
  }
};
</script>

<style>
.edit-form {
  max-width: 50%;
  margin: auto;
}
</style>
