<template>
  <div>
    <template>
      <el-form ref="form" class="text-info " method="POST" @submit.prevent="checkFile" @keyup.enter="checkFile">
        <div v-if="error_form.length" class="text-danger">
          <ul>
            <li v-for="error in error_form" :key="error.index">
              {{ error }}
            </li>
          </ul>
        </div>
        <el-alert
          :title="error_msg"
          type="error"
          v-if=error_msg
        >
        </el-alert>
        <div class="form-group row justify-content-center">
          <el-form ref="uploadfileForm" class="" label-width="200px">
            <el-upload
              class="upload-demo"
              drag
              accept=".xlsx"
              ref="upload" action="" :http-request="handleFile" :on-change="cert_path_file" :multiple="false" :limit="1" :file-list="cert_path"
            >
              <i class="el-icon-upload"></i>
              <div class="el-upload__text">Drop file here or <em>click to upload</em></div>
              <div slot="tip" class="el-upload__tip text-center">Please input excel file (.xlsx).</div>
            </el-upload>
          </el-form>
        </div>
        <div class="form-group row justify-content-center my-3">
          <el-button type="primary" @click="doUpload()" v-if="cert_path.length " >Submit</el-button>
        </div>
      </el-form>
      <div v-if="!success && sent" class="my-2">
        <p class="text-success">Success: {{ valid.length }}</p>
        <p class="text-danger">Failure : {{ invalid.length }}</p>
        <!-- table in here -->
      </div>
      <div class="row">
        <div class="col-12 mt-3">
          <el-table
            :data="resultData"
            style="width: 100%"
            stripe
            header-cell-class-name="bg-header-table"
            :row-class-name="tableRowClassName"
            v-if="resultData.length"
          >

            <el-table-column
              prop="name"
              label="Name"
            >
            </el-table-column>
            <el-table-column
                prop="email"
                label="Email"
                >
            </el-table-column>
             <el-table-column
              prop="phone"
              label="Phone"

            >
            </el-table-column>
            <el-table-column
              prop="status"
              label="Status"
            >
              <template v-slot:default="table">
                <ul>
                  <li
                  v-for="(item, index) in table.row.status"
                  :key="index"
                  >
                  {{item}}
                  </li>
                </ul>
              </template>
            </el-table-column>

          </el-table>
        </div>
      </div>

      <div v-if="sent" class="row mt-3">
        <div class="col-12 d-flex justify-end">
          <el-button type="info" v-show="showbutton" @click="cancelFile()"  class="btn btn-secondary ml-auto text-white mr-2">
            Cancel
          </el-button>

          <el-button type="primary" v-show="showbutton && valid.length !== 0" @click="submitFile()" class="btn btn-info text-white">
            Confirm
          </el-button>
        </div>
      </div>
    </template>
  </div>
</template>
<script>
    import importFileModalServices from '@/services/employee/importFileModal.services'
    import messageRespone from '@/services/employee/responseMessage'

    export default {
        name: 'ImportFileModal',
        middleware: 'authentication',
        data() {
            return {
                data:'',
                files: '',
                success: '',
                error_msg: '',
                valid: '',
                invalid: '',
                sent: false,
                error_form: [],
                showbutton: true,
                cert_path: [],
                resultData: []
            }
        },
        head () {
            return {
                title: 'Import File',
            }
        },
        props: {
          dialogImportFile: Boolean
        },
        methods: {
          async submitFile () {
            this.showbutton = false

            try {
              let responseResult = await importFileModalServices.submitFileAPI(this.data)
              if(responseResult.status === (201 || 200 )&& responseResult.data) {
                this.sent = false
                this.showbutton = false
                this.$emit('update:dialogImportFile', false)
                this.cert_path_file('', [])
              }
            } catch (error) {
              this.showbutton = false
              this.$toast.error(error.response.data.message)
            }
          },
          tableRowClassName({row, rowIndex}) {
            return row.success ? `text-success ${rowIndex}` : `text-danger ${rowIndex}`
          },
          async cancelFile () {
            this.sent = false
            this.cert_path_file('', [])
          },
          handleExceed (files) {
            this.$message.warning(`Selected ${files.length} ${ messageRespone.IMPORT_FILE_TIP}`)
          },
          beforeRemove (file) {
            return this.$confirm(`OK to remove ${file.name}？`)
          },
          handleFile () { },
          cert_path_file (file, fileList) {
            this.cert_path = fileList;
            this.error_msg = ""
            this.resultData = []
          },
          async doUpload () {
            let responseResult = null

            let formData = new FormData()
            this.files = this.cert_path[0] ? this.cert_path[0].raw: ''

            formData.append('file', this.files)
            const re = /.xlsx$/
            if (this.files && !re.test(this.files.name)) {
              this.error_msg = "Please input excel file (.xlsx)"
            } else {
              try {
                responseResult = await importFileModalServices.handleFileUploadAPI(formData)
                if(responseResult && (responseResult.status == 200 && responseResult.data)) {
                  this.resultData = responseResult.data.rows
                  this.data = responseResult.data
                  this.valid = responseResult.data.valid
                  this.invalid = responseResult.data.invalid
                  this.sent = true
                  this.showbutton = true
                }
              } catch (error) {
                this.$toast.error(error.response.data.message)
                this.showbutton = false
              }
            }
          },
        }
    }
</script>
<style>
  .modal-header {
      background-color: #25C9D0;
  }
</style>
