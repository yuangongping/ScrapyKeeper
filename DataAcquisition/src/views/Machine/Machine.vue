<template>
  <div class="app-container"
    v-loading.loading="false"
    element-loading-text="添加服务器中..."
    element-loading-spinner="el-icon-loading"
    element-loading-background="rgba(255, 255, 255, 0.8)">
    <el-table :data="list" v-loading.body="listLoading" element-loading-text="Loading" border fit highlight-current-row>
      <el-table-column label="服务器ip">
        <template slot-scope="scope">
          {{scope.row.url}}
        </template>
      </el-table-column>
      <el-table-column label="服务器类型"  width="200">
        <template slot-scope="scope">
          <span v-if="Number(scope.row.is_master) == 1">
            主服务器
          </span>
          <span  v-else>
            从服务器
          </span>
        </template>
      </el-table-column>
      <el-table-column align="center" label='状态' width="155">
        <template slot-scope="scope">
           <span style="font-weight: 700;" v-if="scope.row.status == 1">
            可用
          </span>
          <span style="color: #999999;" v-else>
            不可用
          </span>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="150" align="center">
        
        <template slot-scope="scope">
          <el-button 
            size="mini" 
            @click="editmachineForm=JSON.parse(JSON.stringify(scope.row)); editmachineFormSubmit=JSON.parse(JSON.stringify(scope.row)); dialogVisible = true;">
            编辑
          </el-button>
          <el-button size="mini" @click="delMachine(scope.row.id)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-button id="add_server" type="primary" @click="dialogFormVisible = true">添加服务器</el-button>

    <el-dialog title="添加服务器" :visible.sync="dialogFormVisible">
      <el-form :model="machineForm" :rules="machineRules" ref="machineForm">
          <el-form-item label="服务器ip" label-width="200" prop="server_ip">
            <el-input name="server_ip" v-model="machineForm.server_ip" auto-complete="off" placeholder="格式: http://172.10.10.183:6800"></el-input>
          </el-form-item>

          <el-form-item label="服务器状态" label-width="200">
            <el-input name="server_status" v-model="machineForm.server_status" auto-complete="off" :disabled="true"></el-input>
          </el-form-item>

          <el-form-item label="是否为主服务器" label-width="200">
            <select v-model="machineForm.is_master" name="is_master">
              <option label="是" value="1">是</option>
              <option label="否" value="0" selected="selected">否</option>
            </select>
          </el-form-item>
       </el-form>
       <div slot="footer" class="dialog-footer">
          <el-button @click="dialogFormVisible = false">取 消</el-button>
          <el-button type="primary" @click="addMachine">添加</el-button>
        </div>
    </el-dialog>

    <el-dialog title="编辑服务器" :visible.sync="dialogVisible" width="600px">
      <el-form :model="editmachineForm" :rules="editmachineRules" ref="editmachineForm">
          <el-form-item label="服务器ip" label-width="200" prop="server_ip">
            <el-input name="server_ip" v-model="editmachineForm.server_ip" auto-complete="off" placeholder="格式: http://172.10.10.183:6800"></el-input>
          </el-form-item>

          <el-form-item label="服务器状态" label-width="200">
            <el-input name="server_status" v-model="editmachineForm.server_status" auto-complete="off" :disabled="true"></el-input>
          </el-form-item>

          <el-form-item label="是否为主服务器" label-width="200">
            <select v-model="editmachineForm.is_master" name="is_master">
              <option label="是" value="1">是</option>
              <option label="否" value="0" selected="selected">否</option>
            </select>
          </el-form-item>
       </el-form>
       <div slot="footer" class="dialog-footer">
          <el-button @click="dialogVisible = false">取 消</el-button>
          <el-button type="primary" @click="editMachine">确定</el-button>
        </div>
     </el-dialog>
  </div>
</template>

<style rel="stylesheet/scss" lang="scss">
  #add_server {
    margin-top: 20px;
  }
</style>

<script>
  import { apiListMachine, apiAddmachine, apiDelMachine, apiEditMachine } from '@/api/machine'
  export default {
    data() {
      return {
        list: [],
        editmachineForm: {},
        editmachineFormSubmit: {},
        machineForm: {
          server_ip: null,
          server_status: '1',
          is_master: 0
        },
        machineRules: {
          server_ip: [{ required: true, message: '请输入服务器地址！', trigger: 'blur' }]
        },
        editmachineRules: {
          server_ip: [{ required: true, message: '请输入服务器地址！', trigger: 'blur' }]
        },
        loading: false,
        listLoading: false,
        dialogFormVisible: false,
        dialogVisible: false
      }
    },
    created() {
      this.listMachine()
    },
    methods: {
      // 获取服务器列表
      async listMachine() {
        this.listLoading = true
        try {
          const res = await apiListMachine()
          this.list = res
        } catch (e) {
          this.$message.error('服务器列表获取错误 ' + e)
        }
        this.listLoading = false
      },

      // 添加服务器
      addMachine() {
        this.$refs.machineForm.validate(async valid => {
          if (valid) {
            this.loading = true
            try {
              const res = await apiAddmachine(this.machineForm)
              if (res.code === 200) {
                this.loading = false
                this.dialogFormVisible = false
                this.listMachine()
              } else {
                this.loading = false
                this.dialogFormVisible = false
              }
            } catch (e) {
              this.loading = false
              this.dialogFormVisible = false
            }
          } else {
            return false
          }
        })
      },

      // 编辑服务器
      async editMachine() {
        this.listLoading = true
        try {
          await apiEditMachine(this.editmachineForm)
          this.listMachine()
        } catch (e) {
          console.log()
        }
        this.listLoading = false
        this.dialogVisible = false
      },

      // 删除服务器
      async delMachine(id) {
        this.listLoading = false
        try {
          const res = await this.$confirm('此操作将永久删除该选项, 是否继续?', '提示', {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }).catch(() => {
            this.$message.error('已取消操作！ ')
          })
          if (res === 'confirm') {
            await apiDelMachine(id)
            this.listMachine()
          } else {
            this.$message.log('已取消操作!')
          }
        } catch (e) {
          this.$message.error('服务器删除错误 ' + e)
        }
      }

    }
  }
</script>
