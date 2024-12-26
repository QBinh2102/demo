import hashlib

from flask import redirect, flash
from flask_admin import Admin, BaseView, expose
from sqlalchemy import func

from app import app, db
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, logout_user
from app.models import NhanVien, HocSinh, DanhSachLop, GiaoVienDayHoc, MonHoc, GiaoVien, UserRole, PhongHoc, QuyDinh, HocKy

admin = Admin(app=app, name='Người Quản Trị', template_mode='bootstrap4')



class DanhSachLopView(ModelView):
    form_columns = ['tenLop', 'hocKy', 'giaoVienChuNhiem', 'phongHoc', 'siSo', 'active']
    column_list = ['tenLop', 'hocKy.namHoc', 'giaoVienChuNhiem', 'phongHoc', 'siSoHienTai', 'siSo', 'active']
    column_labels = {
        'tenLop':'Lớp',
        'hocKy.namHoc': 'Năm học',
        'giaoVienChuNhiem':'Giáo viên chủ nhiệm',
        'phongHoc':'Phòng',
        'siSoHienTai':"Sĩ số lớp",
        'siSo':'Sĩ số tối đa',
        'active':'Trạng thái'
    }

    def get_query(self):
        # Sắp xếp active = True trước, sau đó theo tên lớp
        return self.session.query(self.model).order_by(self.model.active.desc(), self.model.tenLop)

    def get_count_query(self):
        return self.session.query(func.count('*')).select_from(self.model)
    # def on_model_change(self, form, model, is_created):
    #     # Kiểm tra nếu phòng học đã được sử dụng
    #     existing_class = DanhSachLop.query.filter(
    #         DanhSachLop.idPhongHoc == model.idPhongHoc,
    #         DanhSachLop.maDsLop != model.maDsLop  # Không kiểm tra chính lớp hiện tại
    #     ).first()
    #
    #     if existing_class:
    #         flash(f"Phòng học {model.phongHoc.tenPhong} đã được sử dụng trong lớp khác.", "error")
    #         raise ValueError(f"Phòng học {model.phongHoc.tenPhong} đã được chọn.")
    #
    #     super(DanhSachLopView, self).on_model_change(form, model, is_created)


class GiaoVienView(ModelView):
    column_list = ['hoTen', 'gioiTinh', 'ngaySinh', 'diaChi', 'SDT', 'eMail', 'monHoc', 'taiKhoan', 'matKhau']
    form_columns = ['hoTen', 'gioiTinh', 'ngaySinh', 'diaChi', 'SDT', 'eMail', 'taiKhoan', 'matKhau', 'monHoc']
    column_labels = {
        'hoTen': 'Họ tên',
        'gioiTinh': 'Giới tính',
        'ngaySinh': 'Ngày sinh',
        'diaChi': 'Địa chỉ',
        'SDT': 'Số điện thoại',
        'eMail': 'Email',
        'monHoc': 'Môn học',
        'taiKhoan': 'Tài khoản ',
        'matKhau': 'Mật khẩu'
    }

    def on_model_change(self, form, model, is_created):
        if form.matKhau.data:
            model.matKhau = hashlib.md5(form.matKhau.data.encode('utf-8')).hexdigest()

        super(GiaoVienView, self).on_model_change(form, model, is_created)

class NhanVienView(ModelView):
    #form_columns = ['hoTen', 'gioiTinh', 'ngaySinh', 'diaChi', 'SDT', 'eMail', 'taiKhoan', 'matKhau', 'vaiTro']

    column_labels = {
        'hoTen': 'Họ tên',
        'gioiTinh': 'Giới tính',
        'ngaySinh': 'Ngày sinh',
        'diaChi': 'Địa chỉ',
        'SDT': 'Số điện thoại',
        'eMail': 'Email',
        'taiKhoan': 'Tài khoản',
        'matKhau': 'Mật khẩu',
        'vaiTro': 'Vai trò'
    }

    def on_model_change(self, form, model, is_created):
        if form.matKhau.data:
            model.matKhau = hashlib.md5(form.matKhau.data.encode('utf-8')).hexdigest()

        super(NhanVienView, self).on_model_change(form, model, is_created)

class GiaoVienDayHocView(ModelView):
    column_list = ['hoc_ky.namHoc', 'giaoVien', 'giaoVien.monHoc', 'lopDay']
    column_labels = {
        'hoc_ky.namHoc': 'Năm học',
        'giaoVien': 'Giáo Viên',
        'lopDay': 'Lớp',
        'giaoVien.monHoc': 'Môn Học'
    }

    can_create = False  # Không cho phép thêm
    can_delete = False  # Không cho phép xóa

    def get_query(self):
        # Thực hiện sắp xếp năm học giảm dần
        return (
            self.session.query(self.model)
            .join(HocKy, HocKy.idHocKy == self.model.idHocKy)  # JOIN với bảng HocKy
            .order_by(HocKy.namHoc.desc())  # Sắp xếp theo năm học giảm dần
        )

    def get_count_query(self):
        return self.session.query(func.count('*')).select_from(self.model)

class HocSinhView(ModelView):
    form_columns = ['hocSinhLop', 'hoTen', 'gioiTinh','ngaySinh', 'khoi','diaChi','SDT','eMail']
    column_list = ['hoTen', 'gioiTinh', 'ngaySinh', 'khoi','diaChi','SDT','eMail','hocSinhLop']
    column_labels = {
        'hoTen': 'Họ tên',
        'gioiTinh': 'Giới tính',
        'ngaySinh': 'Ngày sinh',
        'khoi':'Khối',
        'diaChi':'Địa chỉ',
        'SDT':'Số điện thoại',
        'hocSinhLop':'Học lớp'
    }
    can_create = False  # Không cho phép thêm

    # def on_model_change(self, form, model, is_created):
    #     dsKhoiPhong = KhoiPhong.query.all()
    #     for khoiphong in dsKhoiPhong:
    #         if(form.KhoiLop.data.__eq__(khoiphong.KhoiLop) and form.PhongHoc.data.__eq__(khoiphong.PhongHoc)
    #             and form.buoiHoc.data.__eq__(khoiphong.buoiHoc)):
    #             flash("Khối phòng đó đã được tạo", "error")
    #             is_created==False
    #             return redirect('/admin/khoiphong/new')
    #
    #     super(GiaoVienView, self).on_model_change(form, model, is_created)
    #
    # def on


class QuiDinhView(ModelView):
    column_labels = {
        'min_age': 'Tuổi thấp nhất',
        'max_age': 'Tuổi cao nhất',
        'si_so': 'Sĩ số'
    }
    can_create = False  # Không cho phép thêm
    can_delete = False  # Không cho phép xóa

    # Chỉ định các cột hiển thị và chỉnh sửa
    form_columns = ['min_age', 'max_age', 'si_so']
    column_list = ['min_age', 'max_age', 'si_so']

admin.add_view(QuiDinhView(QuyDinh, db.session))
admin.add_view(ModelView(MonHoc, db.session))
admin.add_view(ModelView(PhongHoc, db.session))
admin.add_view(NhanVienView(NhanVien, db.session))
admin.add_view(GiaoVienView(GiaoVien, db.session))
admin.add_view(GiaoVienDayHocView(GiaoVienDayHoc, db.session))
admin.add_view(HocSinhView(HocSinh, db.session))
admin.add_view(DanhSachLopView(DanhSachLop, db.session))

