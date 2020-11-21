from connection import PostgresDBManager
import json

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def get_car_list():
    query = """
    select a.desc as brand, b.desc as model, c.desc as variant, d.desc as sku, d.is_sku_default, d2.desc as location, d2.is_location_default,d1.otr, d1.discount, 
    d1.otr_nett, c4.finance_service, c4.monthly_installment, c1.cc_kendaraan, c2.desc as transmission, c3.desc as fuel, d3.image_url as variant_img_url, 
    concat(trim(a.desc), ' ', trim(b.desc), ' ', trim(c.desc)) as keyword,
    a.id as brand_id, b.id as model_id, c.id as variant_id, d.id as sku_id, c2.id as transmission_id, c3.id as fuel_id, 
    c4.simulation_id, c4.finance_service_id, d2.id as location_id, d1.id as price_id
    from car.mst_brand as a
    inner join car.mst_model as b on b.brand_id = a.id and b.is_deleted = false
    inner join car.mst_variant as c on c.model_id = b.id and c.is_deleted = false
    inner join car.mst_variant_specification as c1 on c1.variant_id = c.id and c1.is_active = true
    inner join car.mst_variant_transmission as c2 on c2.id = c1.transmission_id and c2.is_deleted = false
    inner join car.mst_variant_fuel as c3 on c3.id = c1.fuel_id and c3.is_deleted = false
    inner join (
        select * from
        (
            select a.id as simulation_id, a.variant_id, a.finance_service_id, b.desc as finance_service, a.monthly_installment, 
            rank () over (
                partition by a.variant_id
                order by a.monthly_installment asc
            ) as ranking  
            from car.mst_variant_simulation_credit as a
            inner join finance.mst_service as b on b.id = a.finance_service_id and b.is_deleted = false
            where a.is_deleted = false
        ) as rank
        where ranking = 1
    ) as c4 on c4.variant_id = c.id
    inner join car.mst_sku as d on d.variant_id = c.id and c.is_deleted = false
    inner join car.mst_sku_price as d1 on d1.sku_id = d.id and d1.is_deleted = false
    inner join car.mst_sku_location d2 on d2.id = d1.location_id and d2.is_deleted = false
    left join car.mst_sku_image d3 on d3.sku_id = d.id and d3.sequence = 1 and d3.is_deleted = false
    where a.is_deleted = false
    """
    with PostgresDBManager(query,None,False) as cursor:
        data=dictfetchall(cursor)
        return data