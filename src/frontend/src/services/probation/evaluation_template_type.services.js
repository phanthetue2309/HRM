import BaseService from "../base"

class EvaluationTemplateTypeServices extends  BaseService{
    get entity(){
        return "probation/evaluation_template_type";
    }

    async getAll(){
        return await this.request().get(`${this.entity}`);
    }

    async add(data){
        return await this.request().post(`${this.entity}`, data);
    }

    async edit(id, data) {
        return await this.request().put(`${this.entity}/${id}`, data);
    }

    async delete(id) {
        return await this.request().delete(`${this.entity}/${id}`);
    }
}

export default new EvaluationTemplateTypeServices();
